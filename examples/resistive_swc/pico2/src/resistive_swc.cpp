/*
 *  Copyright (C) Hudiy Project - All Rights Reserved
 */

#include "hardware/adc.h"
#include "hardware/watchdog.h"
#include "pico/stdlib.h"
#include "pico/time.h"
#include "tusb.h"

#include <cstdint>

namespace
{
enum class AdcId : uint8_t
{
    ADC1 = 1,
    ADC2 = 2,
};

#pragma pack(push, 1)
struct AdcMessage
{
    uint8_t adcId;
    uint16_t value;
};
#pragma pack(pop)

constexpr uint ADC1_PIN = 26;
constexpr uint ADC2_PIN = 27;
constexpr uint32_t ADC_POLL_RATE_MS = 10;
constexpr uint32_t ADC_MUX_SETTLING_TIME_US = 2;

void sendAdc(AdcId id, uint16_t value)
{
    if(!tud_cdc_connected() || tud_cdc_write_available() < sizeof(AdcMessage))
    {
        return;
    }

    AdcMessage msg;
    msg.adcId = static_cast<uint8_t>(id);
    msg.value = value;

    tud_cdc_write(&msg, sizeof(AdcMessage));
}

bool usbMonitorConnection(struct repeating_timer* t)
{
    if(!tud_cdc_connected())
    {
        watchdog_reboot(0, 0, 0);
    }
    return true;
}
}  // namespace

int main()
{
    adc_init();

    adc_gpio_init(ADC1_PIN);
    gpio_pull_up(ADC1_PIN);

    adc_gpio_init(ADC2_PIN);
    gpio_pull_up(ADC2_PIN);

    tusb_init();

    while(!tud_cdc_connected())
    {
        tud_task();
        sleep_ms(10);
    }

    struct repeating_timer timer;
    add_repeating_timer_ms(1000, usbMonitorConnection, nullptr, &timer);

    uint32_t lastAdcReadMs = 0;

    while(true)
    {
        tud_task();

        uint32_t currentMs = to_ms_since_boot(get_absolute_time());

        if(currentMs - lastAdcReadMs >= ADC_POLL_RATE_MS)
        {
            lastAdcReadMs = currentMs;

            adc_select_input(0);
            sleep_us(ADC_MUX_SETTLING_TIME_US);
            uint16_t adc1Val = adc_read();
            sendAdc(AdcId::ADC1, adc1Val);

            adc_select_input(1);
            sleep_us(ADC_MUX_SETTLING_TIME_US);
            uint16_t adc2Val = adc_read();
            sendAdc(AdcId::ADC2, adc2Val);

            tud_cdc_write_flush();
        }
    }

    return 0;
}

extern "C"
{
#include "tusb_device_descriptors.inl"
}