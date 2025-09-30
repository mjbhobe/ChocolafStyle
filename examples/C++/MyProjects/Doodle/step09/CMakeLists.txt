# CMakeLists.txt for step09 (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)

#if (WIN32 AND NOT USE_MSYS2)
#    set(CMAKE_C_COMPILER "C:/Dev/llvm-mingw-20250925-ucrt-x86_64/bin/gcc.exe")
#    set(CMAKE_CXX_COMPILER "C:/Dev/llvm-mingw-20250925-ucrt-x86_64/bin/g++.exe")
#endif ()

project(step09 LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Sources (from .pro)
set(STEP09_HEADERS
  DrawWindow.h
  Doodle.h
  Line.h
  MainWindow.h
)

set(STEP09_SOURCES
  DrawWindow.cc
  Doodle.cc
  Line.cc
  MainWindow.cc
  step09.cc
)

set(STEP09_RESOURCES
  resources.qrc
)

# --- Executable
add_executable(step09
  ${STEP09_SOURCES}
  ${STEP09_HEADERS}         # headers listed for IDE visibility
  ${STEP09_RESOURCES}
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(step09 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(step09 PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(step09 PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )
