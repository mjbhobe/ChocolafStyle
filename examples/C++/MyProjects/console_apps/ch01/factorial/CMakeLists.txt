# CMakeLists.txt
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)
project(factorial LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
# This defines the INTERFACE target: chocolaf_settings
# and sets Qt, compile options, include dirs, third-party libs, etc.
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common_console.cmake")

#set(PROJECT_HEADERS
#    factorial.h
#)

set(PROJECT_SOURCES
  factorial.cc
)

# --- Executable
add_executable(factorial
  ${PROJECT_SOURCES}
  ${PROJECT_HEADERS}      # headers listed for IDE visibility
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(factorial PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(factorial PRIVATE chocolaf_console_settings)


