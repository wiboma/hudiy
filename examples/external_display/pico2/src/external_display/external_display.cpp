/*
 *  Copyright (C) Hudiy Project - All Rights Reserved
 */

#include "hardware/dma.h"
#include "hardware/watchdog.h"
#include "pico/multicore.h"
#include "pico/stdlib.h"
#include "pico/time.h"

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <string.h>

extern "C"
{
#if defined(LCD_480x320)
#include "3rdparty/lcd_480x320/LCD_Driver.h"
#elif defined(LCD_320x240)
#include "3rdparty/lcd_320x240/LCD_Driver.h"
#elif defined(LCD_240x240)
#include "3rdparty/lcd_240x240/LCD_Driver.h"
#elif defined(LCD_128x160)
#include "3rdparty/lcd_128x160/LCD_Driver.h"
#else
#error "Unknown LCD variant."
#endif

#include "tusb.h"
}

#include "3rdparty/jpegdec/JPEGDEC.h"

namespace
{
enum class MessageId : uint8_t
{
    INVALID = 0,
    FRAME_TILE = 1,
};

#pragma pack(push, 1)
struct MessageHeader
{
    uint32_t payloadSize;
    uint8_t messageId;
};
#pragma pack(pop)

int dmaTxChannel;
int dmaRxChannel;
uint16_t dummyRxWord;

constexpr size_t JPEG_RING_SIZE = 32 * 1024;
static_assert((JPEG_RING_SIZE & (JPEG_RING_SIZE - 1)) == 0, "JPEG_RING_SIZE must be power of two");

alignas(4) uint8_t jpegRingBuffer[JPEG_RING_SIZE];
std::atomic<uint32_t> jpegRingWritePos{0};
std::atomic<uint32_t> jpegRingReadPos{0};
uint32_t jpegStreamPosition = 0;
uint32_t currentJpegSize = 0;
JPEGDEC jpeg;

uint16_t currentXOffset = 0;
uint16_t currentYOffset = 0;

static inline void dmaSpiWaitForFinish()
{
    dma_channel_wait_for_finish_blocking(dmaTxChannel);
    while(spi_is_busy(SPI_PORT))
    {
    }
}

bool usbMonitorConnection(struct repeating_timer* t)
{
    if(!tud_cdc_connected())
    {
        watchdog_reboot(0, 0, 0);
    }
    return true;
}

void usbRead(uint8_t* buffer, size_t length)
{
    size_t totalRead = 0;

    while(totalRead < length)
    {
        tud_task();

        if(const auto available = tud_cdc_n_available(0))
        {
            const auto toRead = std::min<size_t>(length - totalRead, available);
            totalRead += tud_cdc_n_read(0, buffer + totalRead, toRead);
        }
    }
}

static inline uint32_t jpegRingBufferAvailableRead()
{
    return jpegRingWritePos.load(std::memory_order_acquire)
           - jpegRingReadPos.load(std::memory_order_relaxed);
}

static inline uint32_t jpegRingBufferAvailableWrite()
{
    return JPEG_RING_SIZE
           - (jpegRingWritePos.load(std::memory_order_relaxed)
              - jpegRingReadPos.load(std::memory_order_acquire));
}

void jpegRingBufferRead(uint8_t* data, uint32_t length)
{
    uint32_t bytesRead = 0;

    while(bytesRead < length)
    {
        const auto available = jpegRingBufferAvailableRead();
        if(available > 0)
        {
            auto chunk = length - bytesRead;
            if(chunk > available)
            {
                chunk = available;
            }

            const auto currentReadPos = jpegRingReadPos.load(std::memory_order_relaxed);
            const auto readIndex = currentReadPos & (JPEG_RING_SIZE - 1);
            auto firstPart = JPEG_RING_SIZE - readIndex;

            if(firstPart > chunk)
            {
                firstPart = chunk;
            }

            memcpy(data + bytesRead, &jpegRingBuffer[readIndex], firstPart);

            if(chunk > firstPart)
            {
                memcpy(data + bytesRead + firstPart, jpegRingBuffer, chunk - firstPart);
            }

            jpegRingReadPos.store(currentReadPos + chunk, std::memory_order_release);
            bytesRead += chunk;
        }
        else
        {
            __wfe();
        }
    }
}

void jpegRingBufferWrite(uint32_t length)
{
    auto remaining = length;

    while(remaining > 0)
    {
        tud_task();

        const auto availableUsb = tud_cdc_n_available(0);
        const auto availableRingBuffer = jpegRingBufferAvailableWrite();

        const auto currentWritePos = jpegRingWritePos.load(std::memory_order_relaxed);
        const auto writeIndex = currentWritePos & (JPEG_RING_SIZE - 1);

        const auto chunk
            = std::min({availableUsb, availableRingBuffer, remaining, JPEG_RING_SIZE - writeIndex});

        if(chunk > 0)
        {
            if(const auto readBytes = tud_cdc_n_read(0, &jpegRingBuffer[writeIndex], chunk))
            {
                jpegRingWritePos.store(currentWritePos + readBytes, std::memory_order_release);
                __sev();
                remaining -= readBytes;
            }
        }
    }
}

int32_t jpegStreamRead(JPEGFILE* pFile, uint8_t* pBuf, int32_t iLen)
{
    auto bytesToRead = iLen;

    if(jpegStreamPosition + bytesToRead > currentJpegSize)
    {
        bytesToRead = currentJpegSize - jpegStreamPosition;
    }

    if(bytesToRead > 0)
    {
        jpegRingBufferRead(pBuf, bytesToRead);
        jpegStreamPosition += bytesToRead;
    }

    return bytesToRead;
}

int32_t jpegStreamSeek(JPEGFILE* pFile, int32_t iPosition)
{
    return 0;
}

void jpegStreamClose(void* pHandle)
{
}

int jpegStreamDraw(JPEGDRAW* pDraw)
{
    dmaSpiWaitForFinish();
    LCD_DataEnd();

    const auto globalX = currentXOffset + pDraw->x;
    const auto globalY = currentYOffset + pDraw->y;
    LCD_SetWindow(globalX, globalY, globalX + pDraw->iWidth, globalY + pDraw->iHeight);

    LCD_DataStart();
    const auto dataSize = pDraw->iWidth * pDraw->iHeight * 2;
    dma_channel_set_trans_count(dmaRxChannel, dataSize, true);
    dma_channel_set_read_addr(dmaTxChannel, pDraw->pPixels, false);
    dma_channel_set_trans_count(dmaTxChannel, dataSize, true);

    return 1;
}

void renderLoop()
{
    while(true)
    {
        currentJpegSize = multicore_fifo_pop_blocking();

        const uint32_t xyOffsets = multicore_fifo_pop_blocking();
        currentXOffset = xyOffsets & 0xFFFF;
        currentYOffset = xyOffsets >> 16;

        jpegStreamPosition = 0;

        if(jpeg.open(nullptr, currentJpegSize, jpegStreamClose, jpegStreamRead, jpegStreamSeek,
                     jpegStreamDraw))
        {
            jpeg.setPixelType(RGB565_BIG_ENDIAN);
            jpeg.decode(0, 0, JPEG_USES_DMA);
            dmaSpiWaitForFinish();
            LCD_DataEnd();
            jpeg.close();
        }
    }
}

void receiveLoop()
{
    MessageHeader header;

    while(true)
    {
        usbRead(reinterpret_cast<uint8_t*>(&header), sizeof(MessageHeader));

        if(header.messageId == static_cast<uint8_t>(MessageId::FRAME_TILE))
        {
            uint32_t xyOffsets = 0;
            usbRead(reinterpret_cast<uint8_t*>(&xyOffsets), sizeof(xyOffsets));
            const auto jpegSize = header.payloadSize - sizeof(xyOffsets);

            multicore_fifo_push_blocking(jpegSize);
            multicore_fifo_push_blocking(xyOffsets);

            jpegRingBufferWrite(jpegSize);
        }
    }
}
}  // namespace

int main()
{
    System_Init();
    LCD_Init(L2R_U2D);
    tusb_init();

    LCD_Clear(0x0000);

    dmaTxChannel = dma_claim_unused_channel(true);
    auto dmaTxConfig = dma_channel_get_default_config(dmaTxChannel);
    channel_config_set_transfer_data_size(&dmaTxConfig, DMA_SIZE_8);
    channel_config_set_dreq(&dmaTxConfig, spi_get_dreq(SPI_PORT, true));
    channel_config_set_read_increment(&dmaTxConfig, true);
    channel_config_set_write_increment(&dmaTxConfig, false);
    dma_channel_configure(dmaTxChannel, &dmaTxConfig, &spi_get_hw(SPI_PORT)->dr, nullptr, 0, false);

    dmaRxChannel = dma_claim_unused_channel(true);
    auto dmaRxConfig = dma_channel_get_default_config(dmaRxChannel);
    channel_config_set_transfer_data_size(&dmaRxConfig, DMA_SIZE_8);
    channel_config_set_dreq(&dmaRxConfig, spi_get_dreq(SPI_PORT, false));
    channel_config_set_read_increment(&dmaRxConfig, false);
    channel_config_set_write_increment(&dmaRxConfig, false);
    dma_channel_configure(dmaRxChannel, &dmaRxConfig, &dummyRxWord, &spi_get_hw(SPI_PORT)->dr, 0,
                          false);

    while(!tud_cdc_connected())
    {
        tud_task();
        sleep_ms(10);
    }

    struct repeating_timer timer;
    add_repeating_timer_ms(1000, usbMonitorConnection, nullptr, &timer);

    multicore_launch_core1(renderLoop);
    receiveLoop();

    return 0;
}

extern "C"
{
#include "tusb_device_descriptors.inl"
}