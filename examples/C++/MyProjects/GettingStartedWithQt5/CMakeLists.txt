# ========================================================================================
# CMakeLists.txt - multi-target CMake file
#
# To build targets run the following commands in sequence
#
#   prepare build configs - either debug or release 
#   cmake -S . -B cmake-build-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++
#   OR
#   cmake -S . -B cmake-build-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++
#
#   run build
#   cmake --build cmake-build-debug --target targetX && ./cmake-build-debug/build/Release/targetX
#   OR
#   cmake --build cmake-build-release --target targetX && ./cmake-build-release/build/Release/targetX
#
# Author: Manish Bhobe
# My experiments with C/C++, STL and Qt Framework
# Code shared for learning purposes only! Use at your own risk.
# ========================================================================================

cmake_minimum_required(VERSION 3.21)

project(GettingStartedWithQt5 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# pull in all common compiler/linker flags + libs
include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# ----------------------------------------------------------------------------------
# Basic Hello World - Qt Way
# ----------------------------------------------------------------------------------

add_executable(hello_qt_world
        ./hello_qt_world/main.cpp
)

target_include_directories(hello_qt_world PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(hello_qt_world PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Widgets - buttons
# ----------------------------------------------------------------------------------

add_executable(widgets_buttons
        ./widgets/buttons/main.cpp
)

target_include_directories(widgets_buttons PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(widgets_buttons PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Widgets - labels
# ----------------------------------------------------------------------------------

add_executable(widgets_labels
        ./widgets/labels/main.cpp
)

target_include_directories(widgets_labels PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(widgets_labels PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Layouts - grid layouts
# ----------------------------------------------------------------------------------

add_executable(layouts_gridlayout
        ./layouts/gridlayout/main.cpp
)

target_include_directories(layouts_gridlayout PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(layouts_gridlayout PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Layouts - form layouts
# ----------------------------------------------------------------------------------

add_executable(layouts_formlayout
        ./layouts/formlayout/main.cpp
)

target_include_directories(layouts_formlayout PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(layouts_formlayout PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Layouts - vbox layout
# ----------------------------------------------------------------------------------

add_executable(layouts_vboxlayout
        ./layouts/vboxlayout/main.cpp
)

target_include_directories(layouts_vboxlayout PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(layouts_vboxlayout PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Layouts - hbox layout
# ----------------------------------------------------------------------------------

add_executable(layouts_hboxlayout
        ./layouts/hboxlayout/main.cpp
)

target_include_directories(layouts_hboxlayout PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(layouts_hboxlayout PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Custom QMainWindow derived window
# ----------------------------------------------------------------------------------

add_executable(windows_and_dialogs_mainwin
    ./windows_and_dialogs/mainwindow/main.cpp
    ./windows_and_dialogs/mainwindow/mainwindow.h
    ./windows_and_dialogs/mainwindow/mainwindow.cpp
)

target_compile_definitions(windows_and_dialogs_mainwin PRIVATE
    # IMAGES_PATH="${IMAGES_PATH}"
    IMAGES_PATH="${CMAKE_CURRENT_SOURCE_DIR}/windows_and_dialogs/mainwindow"
)

target_include_directories(windows_and_dialogs_mainwin PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(windows_and_dialogs_mainwin PRIVATE chocolaf_settings)

# ----------------------------------------------------------------------------------
# Custom QMainWindow derived window with data entry form
# ----------------------------------------------------------------------------------

add_executable(windows_and_dialogs_mainwin_form
    ./windows_and_dialogs/mainwindow_form/main.cpp
    ./windows_and_dialogs/mainwindow_form/mainwindow.h
    ./windows_and_dialogs/mainwindow_form/mainwindow.cpp
)

target_compile_definitions(windows_and_dialogs_mainwin_form PRIVATE
    # IMAGES_PATH="${IMAGES_PATH}"
    IMAGES_PATH="${CMAKE_CURRENT_SOURCE_DIR}/windows_and_dialogs/mainwindow_form"
)

target_include_directories(windows_and_dialogs_mainwin_form PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(windows_and_dialogs_mainwin_form PRIVATE chocolaf_settings)

