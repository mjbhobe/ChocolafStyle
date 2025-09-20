# CMakeLists.txt for step08 (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)
project(step08 LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Sources (from .pro)
set(STEP08_HEADERS
  DrawWindow.h
  Doodle.h
  Line.h
  MainWindow.h
)

set(STEP08_SOURCES
  DrawWindow.cc
  Doodle.cc
  Line.cc
  MainWindow.cc
  step08.cc
)

set(STEP08_RESOURCES
  resources.qrc
)

# --- Executable
add_executable(step08
  ${STEP08_SOURCES}
  ${STEP08_HEADERS}         # headers listed for IDE visibility
  ${STEP08_RESOURCES}
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(step08 PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(step08 PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(step08 PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )

