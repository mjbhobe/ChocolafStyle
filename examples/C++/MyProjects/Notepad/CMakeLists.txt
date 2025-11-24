# CMakeLists.txt for step09 (converted from qmake .pro)
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module.

cmake_minimum_required(VERSION 3.21)

# Step01 - give a name to your project (== name of EXE built)
# [Tip: give it the same name as your executable]
set(PROJECT_NAME qtpad)

project(${PROJECT_NAME} LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# Step02 -- list the header files, if any
set(PROJECT_HEADERS
  # insert all header file names here (leave blank if none)
)

# Step03 -- list the source files (C/C++) files
set(PROJECT_SOURCES
  # insert all C/C++ file names here
)

# Step04 -- list the GUI form (*.ui) files, if any
set(PROJECT_UI_FILES
  # insert all UI files, if any
)

# Step04 -- list the resource (*.qrc) files, if any
set(PROJECT_RESOURCES
  # insert all QRC files (leave blank if none)
)

# --- Executable dependencies -----------------------------
add_executable(${PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${PROJECT_HEADERS}
    ${PROJECT_UI_FILES}
    ${PROJECT_RESOURCES_FILES}
    ${CHOCOLAF_QT_RESOURCES}
)

# Keep the current dir in include paths for this target.
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(${PROJECT_NAME} PRIVATE chocolaf_settings)
