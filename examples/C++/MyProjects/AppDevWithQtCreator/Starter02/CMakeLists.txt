# CMakeLists.txt
# Builds an executable and consumes the shared "chocolaf_settings" interface
# defined in the global settings module $CHOCOLAF_COMMONFILES_HOME/common.cmake

cmake_minimum_required(VERSION 3.21)

# Step1: change name of your project
# [Tip: give it the same name as your executable]
set(PROJECT_NAME Starter02)

project(${PROJECT_NAME} LANGUAGES CXX)

# --- Include the global settings module (converted from common.pro)
include("$ENV{CHOCOLAF_COMMONFILES_HOME}/common.cmake")

# Step2: add dependencies of your project under these sub-sections

set(PROJECT_HEADERS
    # list all H (header) files here (leave empty if no headers!)
    # NOTE: file names are case sensitive (especially on *nix)
    mainWindow.h
    Counter.h
)

set(PROJECT_SOURCES
    # list all source files (*.c | *.cpp)
    # NOTE: file names are case sensitive (especially on *nix)
    mainWindow.cpp
    Counter.cpp
    main.cpp
)

set(PROJECT_UI_FILES
    # list all UI (forms etc) files here (leave empty if no UI files)
    # NOTE: file names are case sensitive (especially on *nix)
    mainWindow.ui
)

set(PROJECT_RESOURCES_FILES
    # list all resources files here (*.qrc) (leave empty if no qrc files)
    # NOTE: file names are case sensitive (especially on *nix)
)

# --- Executable dependencies -----------------------------
add_executable(${PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${PROJECT_HEADERS}
    ${PROJECT_UI_FILES}
    ${PROJECT_RESOURCES_FILES}
    ${CHOCOLAF_QT_RESOURCES}  # ensure .qrc gets compiled (AUTORCC is ON in the module)
)

# Keep the current dir in include paths for this target.
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(${PROJECT_NAME} PRIVATE chocolaf_settings)

