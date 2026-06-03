# CMakeLists.txt for ImageEditor (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)

set(MY_TARGET_NAME PortfolioViewer)
project(${MY_TARGET_NAME} LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
#     This defines the INTERFACE target: chocolaf_settings
#     and sets Qt, compile options, include dirs, third-party libs, etc.
#include(../../../../../chocolaf/common_files/common.cmake)
message(STATUS "CHOCOLAF_COMMONFILES_HOME = $ENV{CHOCOLAF_COMMONFILES_HOME}")
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# --- Header files, if any (your own *.h files) -----
set(PROJECT_HEADERS
  MainWindow.h
  DataFetcher.h
  PortfolioModel.h
)

# --- Source files, if any (your own *.cpp files) -----
set(PROJECT_SOURCES
  main.cpp
  MainWindow.cpp
  DataFetcher.cpp
  PortfolioModel.cpp
)

# --- Source files, if any (your own *.qrc files) -----
set(PROJECT_RESOURCES

)

# --- Executable
add_executable(${PROJECT_NAME}
  ${PROJECT_SOURCES}
  ${PROJECT_HEADERS}         # headers listed for IDE visibility
  ${PROJECT_RESOURCES}
  ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(${PROJECT_NAME} PRIVATE chocolaf_settings)

# If you’d rather add the “common” Chocolaf sources explicitly to this target
# (they are already attached as INTERFACE sources on chocolaf_settings, but this
# can help some IDEs/generators), uncomment the following:
#
# target_sources(${PROJECT_NAME} PRIVATE
#   ${CHOCOLAF_COMMON_SOURCES}
#   ${CHOCOLAF_COMMON_HEADERS}
# )

