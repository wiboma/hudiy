/*****************************************************************************
 * | File      	:   LCD_1in54.c
 * | Author      :   Waveshare team
 * | Function    :   Hardware underlying interface
 * | Info        :
 *                Used to shield the underlying layers of each master
 *                and enhance portability
 *----------------
 * |	This version:   V1.0
 * | Date        :   2020-05-20
 * | Info        :   Basic version
 *
 ******************************************************************************/
#ifndef __LCD_2IN_H
#define __LCD_2IN_H

#include "DEV_Config.h"

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>  //itoa()

#define LCD_2IN_HEIGHT 240
#define LCD_2IN_WIDTH 320

#define HORIZONTAL 0
#define VERTICAL 1

#define LCD_2IN_SetBacklight(Value) ;

typedef struct
{
    UWORD WIDTH;
    UWORD HEIGHT;
    UBYTE SCAN_DIR;
} LCD_2IN_ATTRIBUTES;
extern LCD_2IN_ATTRIBUTES LCD_2IN;

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
