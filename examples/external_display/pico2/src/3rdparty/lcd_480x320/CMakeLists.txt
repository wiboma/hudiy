add_library(lcd_480x320 LCD_Driver.c DEV_Config.c)

# target_compile_definitions(lcd_480x320 PRIVATE ENABLE_OVERCLOCKING)

target_include_directories(lcd_480x320 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(lcd_480x320 PUBLIC pico_stdlib hardware_spi)
