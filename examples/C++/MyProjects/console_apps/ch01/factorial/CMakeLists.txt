# CMakeLists.txt for factorial (converted from qmake .pro)

cmake_minimum_required(VERSION 3.21)

set(MY_TARGET_NAME factorial)
project(${MY_TARGET_NAME} LANGUAGES CXX)

message(STATUS "CHOCOLAF_COMMONFILES_HOME = $ENV{CHOCOLAF_COMMONFILES_HOME}")

# --- Pull in global common settinsg for console builds
include ("$ENV{CHOCOLAF_COMMONFILES_HOME}/common_console.cmake")

# --- Header files, if any (your own *.h files) -----
set(PROJECT_HEADERS
)

# --- Source files, if any (your own *.cpp files) -----
set(PROJECT_SOURCES
    factorial.cc
)

# --- Source files, if any (your own *.qrc files) -----
set(PROJECT_RESOURCES

)

# --- Executable  to build -----------------------------
add_executable(${PROJECT_NAME}
    ${PROJECT_SOURCES}
    ${PROJECT_HEADERS}         # headers listed for IDE visibility
    ${PROJECT_RESOURCES}
)

# qmake: INCLUDEPATH += .
# Keep the current dir in include paths for this target.
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

# Link against the global interface so we inherit Qt, flags, include dirs and libs.
target_link_libraries(${PROJECT_NAME} PRIVATE chocolaf_settings)

