/*****************************************************************************
 * | File      	:	DEV_Config.c
 * | Author      :   Waveshare team
 * | Function    :	GPIO Function
 * | Info        :
 *   Provide the hardware underlying interface
 *----------------
 * |	This version:   V1.0
 * | Date        :   2018-01-11
 * | Info        :   Basic version
 *
 ******************************************************************************/
#ifndef _DEV_CONFIG_H_
#define _DEV_CONFIG_H_

#include "hardware/spi.h"
#include "pico/stdlib.h"
#include "stdio.h"

#define UBYTE uint8_t
#define UWORD uint16_t
#define UDOUBLE uint32_t

#define LCD_RST_PIN 15
#define LCD_DC_PIN 8
#define LCD_CS_PIN 9
#define LCD_CLK_PIN 10
#define LCD_BKL_PIN 13
#define LCD_MOSI_PIN 11
#define LCD_MISO_PIN 12
#define TP_CS_PIN 16
#define TP_IRQ_PIN 17
#define SD_CS_PIN 22

#define SPI_PORT spi1
#define MAX_BMP_FILES 25
/*------------------------------------------------------------------------------------------------------*/

void DEV_Digital_Write(UWORD Pin, UBYTE Value);
UBYTE DEV_Digital_Read(UWORD Pin);
void DEV_GPIO_Mode(UWORD Pin, UWORD Mode);
void DEV_GPIO_Init(void);

uint8_t System_Init(void);
void System_Exit(void);
uint8_t SPI4W_Write_Byte(uint8_t value);
uint8_t SPI4W_Read_Byte(uint8_t value);

void Driver_Delay_ms(uint32_t xms);
void Driver_Delay_us(uint32_t xus);

#endif
