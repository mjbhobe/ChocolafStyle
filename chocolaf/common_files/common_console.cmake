# ---------------------------------------------------------------------------
# common_console.cmake
#
# Global settings file for compiler/linker/includes etc.
# This file DOES NOT build anything; it defines an INTERFACE target that
# exports compile options/defines, include paths and link libs for consumers
# Use as include file on your CMakeLists.txt for CONSOLE applications only!
# Converted from common.pro file using OpenAI-GPT-5
# ---------------------------------------------------------------------------

cmake_minimum_required(VERSION 3.21)

# CONFIG += c++23 → CMake standard settings
# NOTE: we'll need a C++ 23 standards compiler!!
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# qmake AUTO features (moc, uic, rcc)
# CONFIG += console → (default in CMake, no GUI bundle)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# QT += core xml sql network ; QT -= gui widgets
find_package(QT NAMES Qt6 REQUIRED COMPONENTS Core Xml Sql Network)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Xml Sql Network)

# INTERFACE target used by all console apps
add_library(chocolaf_console_settings INTERFACE)

# ---------------------------------------------------------------------------
# Global compile definitions (from DEFINES += ...)
# ---------------------------------------------------------------------------
# Warn on using deprecated Qt APIs
target_compile_definitions(chocolaf_console_settings INTERFACE QT_DEPRECATED_WARNINGS)

# DEFINES += QT_DEPRECATED_WARNINGS ; CONFIG(release): DEFINES += QT_NO_DEBUG_OUTPUT
target_compile_definitions(chocolaf_console_settings
    INTERFACE
    QT_DEPRECATED_WARNINGS
    CONSOLE_MODE               # from QMAKE_CXXFLAGS += -DCONSOLE_MODE
    $<$<CONFIG:Release>:QT_NO_DEBUG_OUTPUT>
    $<$<BOOL:WIN32>:NOMINMAX WIN32_LEAN_AND_MEAN>
)

# ---------------------------------------------------------------------------
# Per-compiler/per-config compile options (from QMAKE_CXXFLAGS*)
# ---------------------------------------------------------------------------
# -std=c++23 is implied via CMAKE_CXX_STANDARD, but keep the extra warning knobs.
# qmake: -Wno-deprecated-enum-enum-conversion, -pedantic -Wall, O0/O2, g2/g0
# add -fsanitize=address -fno-omit-frame-pointer to g++/clang++ to debug config
# so AddressSanitizer can detect memory leaks
target_compile_options(chocolaf_console_settings
    INTERFACE
    # Common
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wno-deprecated-enum-enum-conversion>
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    # Debug
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang,AppleClang>>:-O0 -g2 -pedantic>
#    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang,AppleClang>>:-fsanitize=address -fno-omit-frame-pointer>
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:MSVC>>:/Od /Z7>
    # Release
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:GNU,Clang,AppleClang>>:-O2 -g0>
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:MSVC>>:/O2 /Z7-> # strip symbols
)

# DEPENDPATH += . ; INCLUDEPATH += .
# INCLUDEPATH += $${COMMON_FILES_HOME}/common_files
if (WIN32)
  set(COMMON_FILES_HOME "c:/Dev/Code/git-projects/ChocolafStyle/chocolaf"
      CACHE PATH "Common files root (Windows)")
else ()
  set(COMMON_FILES_HOME "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf"
      CACHE PATH "Common files root (Unix)")
endif ()

target_include_directories(chocolaf_console_settings
    INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${COMMON_FILES_HOME}/common_files
)

# ---------------------------------------------------------------------------
# Optional MSYS2 vs non-MSYS2 Windows toggles (mirrors the qmake branches)
# ---------------------------------------------------------------------------
# use the -DUSE_MSYS2=ON/OFF flag on command line also, by default it's off\
# Example: cmake -S . -B build -DUSE_MSYS2=ON/OFF
option(USE_MSYS2 "Use MSYS2 layout on Windows" OFF)

if (WIN32)
  if (USE_MSYS2)
    message(STATUS "Using MSYS2 configuration (console)")
    target_include_directories(chocolaf_console_settings INTERFACE
        "C:/Dev/msys64/mingw64/include"
        "C:/Dev/msys64/mingw64/include/opencv4"
        "C:/Dev/GNULibs/fmt/bin/include"
        "C:/Dev/GNULibs/libpqxx/bin/include"
        "C:/Dev/PostgreSQL/15/include"
    )
    link_directories(
        "C:/Dev/msys64/mingw64/lib"
        "C:/Dev/GNULibs/fmt/bin/lib"
        "C:/Dev/GNULibs/libpqxx/bin/lib"
        "C:/Dev/PostgreSQL/15/lib"
    )
    # OPENCV_LIBS = -lopencv_core ...
    set(_OPENCV_MANUAL_LIBS
        opencv_core opencv_imgproc opencv_highgui opencv_ml opencv_video
        opencv_features2d opencv_calib3d opencv_objdetect opencv_videoio
        opencv_imgcodecs opencv_flann
    )
  else ()
    message(STATUS "**NOT** using MSYS2 configuration (console)")
    target_include_directories(chocolaf_console_settings INTERFACE
        "C:/Dev/GNULibs/gmp-6.3.0/bin/include"
        "C:/Dev/OpenCV/build/x86/mingw/install/include"
        "C:/Dev/GNULibs/fmt/bin/include"
        "C:/Dev/GNULibs/libpqxx/include"
        "C:/Dev/PostgreSQL/15/include"
        "C:/Dev/eigen-5.0.0"
    )
    link_directories(
        "C:/Dev/GNULibs/gmp-6.3.0/bin/lib"
        "C:/Dev/OpenCV/build/x86/mingw/install/x64/mingw/lib"
        "C:/Dev/GNULibs/fmt/bin/lib"
        "C:/Dev/GNULibs/libpqxx/lib"
        "C:/Dev/PostgreSQL/15/lib"
    )
    set(_OPENCV_MANUAL_LIBS
        opencv_core451 opencv_imgproc451 opencv_highgui451 opencv_ml451 opencv_video451
        opencv_features2d451 opencv_calib3d451 opencv_objdetect451 opencv_videoio451
        opencv_imgcodecs451 opencv_flann451
    )
  endif ()
else ()
  # unix { INCLUDEPATH += /usr/local/include ; INCLUDEPATH += /usr/include/opencv4 }
  message(STATUS "Settings for Linux build (console)")
  target_include_directories(chocolaf_console_settings INTERFACE
      "/usr/local/include"
      "/usr/include/opencv4"
      "/usr/include/eigen-5.0.0"
  )
  set(_OPENCV_MANUAL_LIBS
      opencv_core opencv_imgproc opencv_highgui opencv_ml opencv_video
      opencv_features2d opencv_calib3d opencv_objdetect opencv_videoio
      opencv_imgcodecs opencv_flann
  )
endif ()

# FMT, OpenCV, PostgreSQL, libpqxx, GMP
# (QMAKE_LIBS += $${QMAKE_LIB_DIRS} $${STD_LIBS} $${GMP_LIBS} $${OPENCV_LIBS})
find_package(fmt QUIET)
if (fmt_FOUND)
  target_link_libraries(chocolaf_console_settings INTERFACE fmt::fmt)
endif ()

find_package(OpenCV QUIET COMPONENTS core imgproc highgui ml video features2d calib3d objdetect videoio imgcodecs flann)
if (OpenCV_FOUND)
  target_include_directories(chocolaf_console_settings INTERFACE ${OpenCV_INCLUDE_DIRS})
  target_link_libraries(chocolaf_console_settings INTERFACE ${OpenCV_LIBS})
else ()
  target_link_libraries(chocolaf_console_settings INTERFACE ${_OPENCV_MANUAL_LIBS})
endif ()

find_package(PostgreSQL QUIET)
if (PostgreSQL_FOUND)
  target_include_directories(chocolaf_console_settings INTERFACE ${PostgreSQL_INCLUDE_DIRS})
  target_link_libraries(chocolaf_console_settings INTERFACE ${PostgreSQL_LIBRARIES})
endif ()

if (WIN32)
  target_link_libraries(chocolaf_console_settings INTERFACE pqxx pq)
else ()
  find_library(PQXX_LIBRARY NAMES pqxx)
  if (PQXX_LIBRARY)
    target_link_libraries(chocolaf_console_settings INTERFACE ${PQXX_LIBRARY})
  endif ()
endif ()

if (WIN32)
  target_link_libraries(chocolaf_console_settings INTERFACE gmp gmpxx)
else ()
  find_library(GMP_LIBRARY NAMES gmp)
  find_library(GMPXX_LIBRARY NAMES gmpxx)
  if (GMP_LIBRARY)
    target_link_libraries(chocolaf_console_settings INTERFACE ${GMP_LIBRARY})
  endif ()
  if (GMPXX_LIBRARY)
    target_link_libraries(chocolaf_console_settings INTERFACE ${GMPXX_LIBRARY})
  endif ()
endif ()

# win32 { LIBS += -lUser32 -lGdi32 -lKernel32 -lDwmapi }
# unix { STD_LIBS = -lm -lstdc++ -lfmt -lpqxx -lpq }
if (WIN32)
  target_link_libraries(chocolaf_console_settings INTERFACE
      user32 gdi32 kernel32 dwmapi wsock32 ws2_32
  )
else ()
  target_link_libraries(chocolaf_console_settings INTERFACE m)
endif ()

# Link Qt modules to interface
target_link_libraries(chocolaf_console_settings
    INTERFACE
    Qt6::Core
    Qt6::Xml
    Qt6::Sql
    Qt6::Network
)

# SOURCES += $$PWD/common_funcs.cpp
# HEADERS += $$PWD/common_funcs.h rapidcsv.h argparse.hpp
set(CHOCOLAF_CONSOLE_SOURCES
    "${CMAKE_CURRENT_LIST_DIR}/common_funcs.cpp"
    CACHE INTERNAL "Console common sources"
)
set(CHOCOLAF_CONSOLE_HEADERS
    "${CMAKE_CURRENT_LIST_DIR}/common_funcs.h"
    "${CMAKE_CURRENT_LIST_DIR}/rapidcsv.h"
    "${CMAKE_CURRENT_LIST_DIR}/argparse/argparse.hpp"
    CACHE INTERNAL "Console common headers"
)

target_sources(chocolaf_console_settings INTERFACE
    ${CHOCOLAF_CONSOLE_SOURCES}
    ${CHOCOLAF_CONSOLE_HEADERS}
)


# qmake also set OBJECTS_DIR/MOC_DIR/RCC_DIR/UI_DIR under DESTDIR.
# CMake manages moc/rcc/uic in its own build tree; overriding their
# directories is uncommon and generally unnecessary, so we omit that here.
# ---------------------------------------------------------------------------

# How to consume this in your CMake project:
#
#   include(${CMAKE_SOURCE_DIR}/cmake/ChocolafGlobal.cmake)
#   add_executable(myapp main.cpp)
#   target_link_libraries(myapp PRIVATE chocolaf_settings)
#   target_sources(myapp PRIVATE ${CHOCOLAF_COMMON_SOURCES} ${CHOCOLAF_QT_RESOURCES})
#   target_include_directories(myapp PRIVATE ${CHOCOLAF_COMMON_HEADERS}) # headers are header-only
#
# If OpenCV/fmt/PostgreSQL/libpqxx aren’t auto-found, either:
#  - set USE_MSYS2 ON and keep the link_directories/include dirs above, or
#  - provide CMAKE_PREFIX_PATH / *_ROOT hints to their installations.

# --- Debug summary for chocolaf_settings ------------------------------------

# 1. Include directories
get_target_property(_choco_includes chocolaf_console_settings INTERFACE_INCLUDE_DIRECTORIES)

# 2. Linked libraries
get_target_property(_choco_libs chocolaf_console_settings INTERFACE_LINK_LIBRARIES)

# 3. Search paths (used by link_directories() etc.)
get_directory_property(_link_dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} LINK_DIRECTORIES)

# 4. Common headers (includes appended ones like QtAwesome.h)
set(_choco_headers "${CHOCOLAF_COMMON_HEADERS}")

# 5. Common sources (includes appended ones like QtAwesome.cpp)
set(_choco_sources "${CHOCOLAF_COMMON_SOURCES}")

# 6. Common resources (all *.qrc files)
set(_choco_resources "${CHOCOLAF_QT_RESOURCES}")

# 7. --- ADDED: Compiler flags applied to this target ---
get_target_property(_choco_compile_opts chocolaf_console_settings INTERFACE_COMPILE_OPTIONS)
get_target_property(_choco_compile_defs chocolaf_console_settings INTERFACE_COMPILE_DEFINITIONS)

# 8. --- ADDED: Linker flags applied to this target ---
get_target_property(_choco_link_opts chocolaf_console_settings INTERFACE_LINK_OPTIONS)

# Flatten for pretty-printing
string(REPLACE ";" "\n    " _includes_str "${_choco_includes}")
string(REPLACE ";" "\n    " _libs_str "${_choco_libs}")
string(REPLACE ";" "\n    " _choco_headers_str "${_choco_headers}")
string(REPLACE ";" "\n    " _choco_sources_str "${_choco_sources}")
string(REPLACE ";" "\n    " _choco_resources_str "${_choco_resources}")
string(REPLACE ";" "\n    " _compile_opts_str "${_choco_compile_opts}")
string(REPLACE ";" "\n    " _compile_defs_str "${_choco_compile_defs}")
string(REPLACE ";" "\n    " _link_opts_str "${_choco_link_opts}")

message(STATUS "====== Chocolaf Common Settings ======")
message(STATUS "Include dirs:\n    ${_includes_str}")
message(STATUS "Library search paths:\n    ${_linkdirs_str}")
message(STATUS "Linked libs:\n    ${_libs_str}")
message(STATUS "Common includes:\n    ${_choco_headers_str}")
message(STATUS "Common sources:\n    ${_choco_sources_str}")
message(STATUS "Common resources:\n    ${_choco_resources_str}")
message(STATUS "Compiler options:\n    ${_compile_opts_str}")
message(STATUS "Compiler definitions:\n    ${_compile_defs_str}")
message(STATUS "Link options:\n    ${_link_opts_str}")

message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_LIBRARY_PATH: ${CMAKE_LIBRARY_PATH}")
message(STATUS "CMAKE_INCLUDE_PATH: ${CMAKE_INCLUDE_PATH}")
message(STATUS "======================================")
