/*****************************************************************************
 * | File      	:   LCD_1in47.c
 * | Author      :   Waveshare team
 * | Function    :   Hardware underlying interface
 * | Info        :
 *                Used to shield the underlying layers of each master
 *                and enhance portability
 *----------------
 * |	This version:   V1.0
 * | Date        :   2022-03-08
 * | Info        :   Basic version
 *
 ******************************************************************************/
#ifndef __LCD_1IN47_H
#define __LCD_1IN47_H

#include "DEV_Config.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>  //itoa()

#define LCD_1IN47_HEIGHT 172
#define LCD_1IN47_WIDTH 320

#define HORIZONTAL 0
#define VERTICAL 1

#define LCD_1IN47_SetBacklight(Value) ;

typedef struct
{
    UWORD WIDTH;
    UWORD HEIGHT;
    UBYTE SCAN_DIR;
} LCD_1IN47_ATTRIBUTES;
extern LCD_1IN47_ATTRIBUTES LCD_1IN47;

typedef enum
{
    L2R_U2D = 0,  // 0°
    D2U_L2R,      // 90°
    R2L_D2U,      // 180°
    U2D_R2L,      // 270°
} LCD_SCAN_DIR;
#define SCAN_DIR_DFT L2R_U2D  // Default scan direction = L2R_U2D

/********************************************************************************
function:
            Macro definition variable name
********************************************************************************/
void LCD_Init(LCD_SCAN_DIR Scan_dir);
void LCD_Clear(UWORD Color);
void LCD_SetWindow(UWORD Xstart, UWORD Ystart, UWORD Xend, UWORD Yend);
void LCD_1IN47_Display(UWORD* Image);
void LCD_1IN47_DisplayWindows(UWORD Xstart, UWORD Ystart, UWORD Xend, UWORD Yend, UWORD* Image);
void LCD_1IN47_DisplayPoint(UWORD X, UWORD Y, UWORD Color);
void Handler_1IN47_LCD(int signo);
void LCD_DataStart();
void LCD_DataEnd();
#endif
