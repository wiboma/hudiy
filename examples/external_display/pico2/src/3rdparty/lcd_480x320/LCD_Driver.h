/*****************************************************************************
 * | File      	:	LCD_Driver.h
 * | Author      :   Waveshare team
 * | Function    :	ILI9486 Drive function
 * | Info        :
 *   Image scanning:
 *      Please use progressive scanning to generate images or fonts
 *----------------
 * |	This version:   V1.0
 * | Date        :   2018-01-11
 * | Info        :   Basic version
 *
 ******************************************************************************/

/**************************Intermediate driver layer**************************/

#ifndef __LCD_DRIVER_H
#define __LCD_DRIVER_H

#include "DEV_Config.h"

#define LCD_2_8 0x52
#define LCD_3_5 0x00

#define COLOR uint16_t   // The variable type of the color (unsigned short)
#define POINT uint16_t   // The type of coordinate (unsigned short)
#define LENGTH uint16_t  // The type of coordinate (unsigned short)

/********************************************************************************
function:
        Define the full screen height length of the display
********************************************************************************/
#define LCD_X_MAXPIXEL 480  // LCD width maximum memory
#define LCD_Y_MAXPIXEL 320  // LCD height maximum memory
#define LCD_X 0
#define LCD_Y 0

#define LCD_3_5_WIDTH (LCD_X_MAXPIXEL - 2 * LCD_X)  // LCD width
#define LCD_3_5_HEIGHT LCD_Y_MAXPIXEL               // LCD height

#define LCD_2_8_WIDTH 240  // LCD width
#define LCD_2_8_HEIGHT 320

/********************************************************************************
function:
            scanning method
********************************************************************************/
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
    Defines the total number of rows in the display area
********************************************************************************/
typedef struct
{
    LENGTH LCD_Dis_Column;  // COLUMN
    LENGTH LCD_Dis_Page;    // PAGE
    LCD_SCAN_DIR LCD_Scan_Dir;
    POINT LCD_X_Adjust;  // LCD x actual display position calibration
    POINT LCD_Y_Adjust;  // LCD y actual display position calibration
} LCD_DIS;

/********************************************************************************
function:
            Macro definition variable name
********************************************************************************/
void LCD_Init(LCD_SCAN_DIR LCD_ScanDir);
void LCD_SetGramScanWay(LCD_SCAN_DIR Scan_dir);
void BMP_SetGramScanWay(LCD_SCAN_DIR Scan_dir);

void LCD_WriteReg(uint8_t Reg);
void LCD_WriteData(uint16_t Data);

void LCD_SetWindow(POINT Xstart, POINT Ystart, POINT Xend, POINT Yend);
void LCD_SetCursor(POINT Xpoint, POINT Ypoint);
void LCD_SetColor(COLOR Color, POINT Xpoint, POINT Ypoint);
void LCD_SetPointlColor(POINT Xpoint, POINT Ypoint, COLOR Color);
void LCD_SetArealColor(POINT Xstart, POINT Ystart, POINT Xend, POINT Yend, COLOR Color);
void LCD_Clear(COLOR Color);
uint8_t LCD_Read_Id(void);
void LCD_DataStart();
void LCD_DataEnd();
#endif
