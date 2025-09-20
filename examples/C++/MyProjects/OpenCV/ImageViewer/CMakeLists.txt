# CMakeLists.txt for ImageViewer (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)
project(ImageViewer LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Sources (from .pro)
set(IMAGEVIEWER_HEADERS
  ImageSpinner.h
  ImageViewer.h
)

set(IMAGEVIEWER_SOURCES
  ImageSpinner.cpp
  ImageViewer.cpp
  main.cpp
)

set(IMAGEVIEWER_RESOURCES
  ImageViewer.qrc
)

# --- Executable
add_executable(ImageViewer
  ${IMAGEVIEWER_SOURCES}
  ${IMAGEVIEWER_HEADERS}         # headers listed for IDE visibility
  ${IMAGEVIEWER_RESOURCES}
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(ImageViewer PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(ImageViewer PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(ImageViewer PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )

