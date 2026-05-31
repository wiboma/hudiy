add_library(jpegdec JPEGDEC.cpp)

target_compile_definitions(jpegdec PRIVATE HAS_SIMD=1)
target_compile_options(jpegdec PRIVATE -O3)
target_include_directories(jpegdec INTERFACE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(jpegdec PRIVATE pico_stdlib cmsis_core)
