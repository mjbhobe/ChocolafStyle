# CMakeLists.txt
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)

# if (WIN32 AND NOT USE_MSYS2)
#  set(CMAKE_C_COMPILER "C:/Dev/llvm-mingw-20250925-ucrt-x86_64/bin/gcc.exe")
#  set(CMAKE_CXX_COMPILER "C:/Dev/llvm-mingw-20250925-ucrt-x86_64/bin/g++.exe")
# endif()

project(hash LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
# This defines the INTERFACE target: chocolaf_settings
# and sets Qt, compile options, include dirs, third-party libs, etc.
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common_console.cmake")

set(PROJECT_HEADERS
   person.h
)

set(PROJECT_SOURCES
   person.cpp
   main.cpp
)

# --- Executable
add_executable(hash
  ${PROJECT_SOURCES}
  ${PROJECT_HEADERS}      # headers listed for IDE visibility
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(hash PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(hash PRIVATE chocolaf_console_settings)
