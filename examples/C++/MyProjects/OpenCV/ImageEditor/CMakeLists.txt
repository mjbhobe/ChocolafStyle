# CMakeLists.txt for ImageEditor (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)
project(ImageEditor LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
message(STATUS "CHOCOLAF_COMMONFILES_HOME = $ENV{CHOCOLAF_COMMONFILES_HOME}")
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Sources (from .pro)
set(IMAGEEDITOR_HEADERS
  ImageSpinner.h
  ImageEditor.h
  MatOps.h
)

set(IMAGEEDITOR_SOURCES
  ImageSpinner.cpp
  ImageEditor.cpp
  MatOps.cpp
  main.cpp
)

set(IMAGEEDITOR_RESOURCES
  ImageEditor.qrc
)

# --- Executable
add_executable(ImageEditor
  ${IMAGEEDITOR_SOURCES}
  ${IMAGEEDITOR_HEADERS}         # headers listed for IDE visibility
  ${IMAGEEDITOR_RESOURCES}
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(ImageEditor PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(ImageEditor PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(ImageEditor PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )

