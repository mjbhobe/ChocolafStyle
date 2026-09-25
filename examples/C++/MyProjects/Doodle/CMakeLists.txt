# ========================================================================================
# CMakeLists.txt - multi-target CMake file
#
# To build targets run the following commands in sequence
#
#   prepare build configs - either debug or release 
#   cmake -S . -B cmake-build-debug -G Ninja -DCMAKE_PREFIX_PATH="~/Qt/lib/cmake" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++
#   OR
#   cmake -S . -B cmake-build-release -G Ninja -DCMAKE_PREFIX_PATH="~/Qt/lib/cmake" -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++
#
#   run build
#   cmake --build cmake-build-debug --target targetX && ./cmake-build-debug/build/Debug/targetX
#   OR
#   cmake --build cmake-build-release --target targetX && ./cmake-build-release/build/Release/targetX
#
# Author: Manish Bhobe
# My experiments with C/C++, STL and Qt Framework
# Code shared for learning purposes only! Use at your own risk.
# ========================================================================================

cmake_minimum_required(VERSION 3.21)

project(Scribble LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# pull in all common compiler/linker flags + libs
# include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common_console.cmake")
include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# ----------------------------------------------------------------------------------
# Step 01 - show the basic window
# ----------------------------------------------------------------------------------

add_executable(step01
    ./step01/main.cc
)

target_include_directories(step01 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step01 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 02 - custom main window class
# ----------------------------------------------------------------------------------

add_executable(step02
    ./step02/main.cc
    ./step02/DrawWindow.h
    ./step02/DrawWindow.cc
)

target_include_directories(step02 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step02 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 03 - handling mouse click events
# ----------------------------------------------------------------------------------

add_executable(step03
    ./step03/main.cc
    ./step03/DrawWindow.h
    ./step03/DrawWindow.cc
)

target_include_directories(step03 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step03 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 04 - drawing mouse click points (first attempt!)
# ----------------------------------------------------------------------------------

add_executable(step04
    ./step04/main.cc
    ./step04/DrawWindow.h
    ./step04/DrawWindow.cc
)

target_include_directories(step04 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step04 PRIVATE chocolaf_settings)