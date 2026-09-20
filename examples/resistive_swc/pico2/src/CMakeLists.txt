add_executable(resistive_swc resistive_swc.cpp)
target_compile_options(resistive_swc PRIVATE -O3)

target_include_directories(resistive_swc PRIVATE ${CMAKE_SOURCE_DIR}/src)

target_link_libraries(resistive_swc PRIVATE pico_stdlib hardware_adc
                                            tinyusb_device)

pico_enable_stdio_usb(resistive_swc 0)
pico_enable_stdio_uart(resistive_swc 0)
pico_add_extra_outputs(resistive_swc)
