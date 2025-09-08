# common_console.cmake
#
# Global settings converted from qmake .pro (console, no GUI).
# Defines an INTERFACE target with compile options/defines, include dirs,
# and link libraries. This file does NOT build anything.

cmake_minimum_required(VERSION 3.21)

# --- Language standard (CONFIG c++20, but QMAKE_CXXFLAGS also forced C++23)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Qt components (QT += core xml sql network; QT -= gui/widgets)
# find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Xml Sql Network)
find_package(QT NAMES Qt6 REQUIRED COMPONENTS Core Xml Sql Network)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Xml Sql Network)

# --- The global interface target exported to consumers
add_library(chocolaf_console_settings INTERFACE)

# --- Common include roots (DEPENDPATH+=. INCLUDEPATH+=.)
target_include_directories(chocolaf_console_settings
  INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

# --- COMMON_FILES_HOME (from win32/unix branches in .pro)
if(WIN32)
  set(COMMON_FILES_HOME "c:/Dev/Code/git-projects/ChocolafStyle/chocolaf" CACHE PATH "Common files home (Windows)")
else()
  set(COMMON_FILES_HOME "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf" CACHE PATH "Common files home (Unix)")
endif()

# INCLUDEPATH += $${COMMON_FILES_HOME}/common_files
target_include_directories(chocolaf_console_settings INTERFACE
  "${COMMON_FILES_HOME}/common_files"
)

# --- Compile definitions (DEFINES += ...)
#   QT_DEPRECATED_WARNINGS (always)
#   QT_NO_DEBUG_OUTPUT only for Release
#   -DCONSOLE_MODE (requested in QMAKE_CXXFLAGS)
target_compile_definitions(chocolaf_console_settings
  INTERFACE
    QT_DEPRECATED_WARNINGS
    CONSOLE_MODE
    $<$<CONFIG:Release>:QT_NO_DEBUG_OUTPUT>
)

# --- Compile options (QMAKE_CXXFLAGS*, warnings & opts)
# Note: -std=c++23 handled by CMAKE_CXX_STANDARD above.
target_compile_options(chocolaf_console_settings
  INTERFACE
    # Suppressions & warnings from .pro
    $<$<CXX_COMPILER_ID:Clang,AppleClang>:-Wno-c11-extensions>
    $<$<CXX_COMPILER_ID:Clang,AppleClang,GNU>:-Wno-deprecated-anon-enum-enum-conversion>
    $<$<CXX_COMPILER_ID:Clang,AppleClang,GNU>:-Wno-unused-variable -Wno-unused-parameter -Wall -pedantic>

    # Debug/Release tunings
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:Clang,AppleClang,GNU>>:-O0 -g2>
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:Clang,AppleClang,GNU>>:-O2 -g0>

    # MSVC equivalents (best-effort)
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:MSVC>>:/Od /Z7>
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:MSVC>>:/O2 /Z7>
)

# --- Platform library bits (LIBS += ...)
if(WIN32)
  # -lUser32 -lGdi32 -lKernel32 -lDwmapi
  target_link_libraries(chocolaf_console_settings INTERFACE
    user32 gdi32 kernel32 dwmapi
  )
else()
  # On Unix the .pro’s STD_LIBS included -lm; libstdc++ is implicit with g++/clang++
  target_link_libraries(chocolaf_console_settings INTERFACE m)
endif()

# =========================
# 3rd-party dependencies
# =========================

# MSYS2 vs non-MSYS2 toggles on Windows (mirrors CONFIG(MSYS2))
option(USE_MSYS2 "Use MSYS2 paths for includes/libs on Windows" ON)

if(WIN32)
  if(USE_MSYS2)
    message(STATUS "Using MSYS2 configuration...")
    target_include_directories(chocolaf_console_settings INTERFACE
      "C:/Dev/msys64/mingw64/include"
      "C:/Dev/msys64/mingw64/include/opencv4"
      "C:/Dev/GNULibs/fmt/bin/include"
      "C:/Dev/GNULibs/libpqxx/bin/include" "C:/Dev/PostgreSQL/15/include"
    )
    # link directories
