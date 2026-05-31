/*****************************************************************************
 * | File      	:   LCD_1IN28.h
 * | Author      :   Waveshare team
 * | Function    :   Hardware underlying interface
 * | Info        :
 *                Used to shield the underlying layers of each master
 *                and enhance portability
 *----------------
 * |	This version:   V1.0
 * | Date        :   2020-12-16
 * | Info        :   Basic version
 *
 ******************************************************************************/
#ifndef __LCD_1IN28_H
#define __LCD_1IN28_H

#include "DEV_Config.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>  //itoa()

#define LCD_1IN28_HEIGHT 240
#define LCD_1IN28_WIDTH 240

#define HORIZONTAL 0
#define VERTICAL 1

typedef struct
{
    UWORD WIDTH;
    UWORD HEIGHT;
    UBYTE SCAN_DIR;
} LCD_1IN28_ATTRIBUTES;
extern LCD_1IN28_ATTRIBUTES LCD_1IN28;

typedef enum
{
    L2R_U2D = 0,  // 0°
    D2U_L2R,      // 90°
    R2L_D2U,      // 180°
    U2D_R2L,      // 270°
} LCD_SCAN_DIR;

/********************************************************************************
function:
            Macro definition variable name
********************************************************************************/
void LCD_Init(LCD_SCAN_DIR Scan_dir);
void LCD_Clear(UWORD Color);
void LCD_SetWindow(UWORD Xstart, UWORD Ystart, UWORD Xend, UWORD Yend);
void LCD_DataStart();
void LCD_DataEnd();
#endif
