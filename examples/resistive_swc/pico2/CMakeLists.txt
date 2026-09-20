# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
  set(USERHOME $ENV{USERPROFILE})
else()
  set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if(EXISTS ${picoVscode})
  include(${picoVscode})
endif()
# ====================================================================================
cmake_minimum_required(VERSION 3.25.0)

set(PICO_BOARD
    pico2_w
    CACHE STRING "Board type")
include(pico_sdk_import.cmake)
project(pico_external_display C CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)

pico_sdk_init()

add_subdirectory(src)
