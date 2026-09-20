#========================================================================================
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
#========================================================================================

cmake_minimum_required(VERSION 3.21)

project(Qt6Tutorials LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# pull in all common compiler/linker flags + libs
include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common_console.cmake")
include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# ----------------------------------------------------------------------------------
# Basic Hello World - Qt Way (GUI app)
# ----------------------------------------------------------------------------------

add_executable(hello_world
    ./src/hello_world/main.cpp
)

target_include_directories(hello_world PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(hello_world PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Basic Hello World - Qt Way (console app)
# ----------------------------------------------------------------------------------

add_executable(hello_console_world
    ./src/hello_console_world/main.cpp
    src/hello_console_world/test.h
    src/hello_console_world/test.cpp
)

target_include_directories(hello_console_world PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(hello_console_world PRIVATE chocolaf_console_settings)

# ----------------------------------------------------------------------------------
# QObject and MOC
# ----------------------------------------------------------------------------------

add_executable(signals_and_slots
    ./src/signals_and_slots/main.cpp
    ./src/signals_and_slots/unitConverter.h
    ./src/signals_and_slots/unitConverter.cpp
    ./src/signals_and_slots/conversionObserver.h
    ./src/signals_and_slots/conversionObserver.cpp
)

target_include_directories(signals_and_slots PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(signals_and_slots PRIVATE chocolaf_console_settings)


