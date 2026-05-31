add_library(lcd_320x240 LCD_Driver.c DEV_Config.c)

target_include_directories(lcd_320x240 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(lcd_320x240 PUBLIC pico_stdlib hardware_spi hardware_pwm)
