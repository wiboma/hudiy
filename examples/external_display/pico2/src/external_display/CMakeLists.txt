set(LCD_VARIANTS "LCD_480x320" "LCD_320x240" "LCD_240x240" "LCD_128x160")

foreach(VARIANT ${LCD_VARIANTS})
  string(TOLOWER "${VARIANT}" LCD_LIB_NAME)
  set(TARGET_NAME "external_display_${LCD_LIB_NAME}")

  add_executable(${TARGET_NAME} external_display.cpp)
  target_compile_options(${TARGET_NAME} PRIVATE -O3)
  target_compile_definitions(${TARGET_NAME} PRIVATE ${VARIANT})

  target_include_directories(${TARGET_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/src
                                                    ${CMAKE_CURRENT_SOURCE_DIR})

  target_link_libraries(
    ${TARGET_NAME}
    PRIVATE ${LCD_LIB_NAME}
            ${HARDWARE_LIBS}
            jpegdec
            pico_stdlib
            hardware_dma
            pico_multicore
            tinyusb_device)

  pico_enable_stdio_usb(${TARGET_NAME} 0)
  pico_enable_stdio_uart(${TARGET_NAME} 0)
  pico_add_extra_outputs(${TARGET_NAME})
  pico_set_binary_type(${TARGET_NAME} copy_to_ram)
endforeach()
