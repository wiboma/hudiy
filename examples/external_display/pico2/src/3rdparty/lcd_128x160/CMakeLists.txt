add_library(lcd_128x160 LCD_Driver.c DEV_Config.c)

target_include_directories(lcd_128x160 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(lcd_128x160 PUBLIC pico_stdlib hardware_spi hardware_pwm)
