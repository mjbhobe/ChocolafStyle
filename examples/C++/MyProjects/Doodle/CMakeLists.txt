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

# ----------------------------------------------------------------------------------
# Step 05 - drawing a single doodle
# ----------------------------------------------------------------------------------

add_executable(step05
    ./step05/main.cc
    ./step05/constants.h
    ./step05/DrawWindow.h
    ./step05/DrawWindow.cc
)

target_include_directories(step05 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step05 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 06 - change attributes of a doodle line
# ----------------------------------------------------------------------------------

add_executable(step06
    ./step06/main.cc
    ./step06/constants.h
    ./step06/DrawWindow.h
    ./step06/DrawWindow.cc
    ./step06/Line.h
    ./step06/Line.cc
)

target_include_directories(step06 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step06 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 07 - draw multiple scribbles/doodles
# ----------------------------------------------------------------------------------

add_executable(step07
    ./step07/main.cc
    ./step07/constants.h
    ./step07/DrawWindow.h
    ./step07/DrawWindow.cc
    ./step07/Doodle.h
    ./step07/Doodle.cc
    ./step07/Line.h
    ./step07/Line.cc
)

target_include_directories(step07 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step07 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 08 - draw multiple scribbles/doodles
# ----------------------------------------------------------------------------------

add_executable(step08
    ./step08/main.cc
    ./step08/constants.h
    ./step08/DrawWindow.h
    ./step08/DrawWindow.cc
    ./step08/Doodle.h
    ./step08/Doodle.cc
    ./step08/Line.h
    ./step08/Line.cc
    ./step08/resources.qrc
    ./step08/IconFont.h
)

target_include_directories(step08 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step08 PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Step 09 - draw multiple scribbles/doodles
# ----------------------------------------------------------------------------------

add_executable(step09
    ./step09/main.cc
    ./step09/constants.h
    ./step09/MainWindow.h
    ./step09/MainWindow.cc
    ./step09/DrawWindow.h
    ./step09/DrawWindow.cc
    ./step09/Doodle.h
    ./step09/Doodle.cc
    ./step09/Line.h
    ./step09/Line.cc
    ./step09/resources.qrc
    ./step09/IconFont.h
)

target_include_directories(step09 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(step09 PRIVATE chocolaf_settings)