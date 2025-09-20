# CMakeLists.txt for step05 (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)
project(step03 LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Sources (from .pro)
set(STEP03_HEADERS
  DrawWindow.h
)

set(STEP03_SOURCES
  DrawWindow.cc
  step03.cc
)

# --- Executable
add_executable(step03
  ${STEP03_SOURCES}
  ${STEP03_HEADERS}         # headers listed for IDE visibility
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(step03 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(step03 PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(step05 PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )

