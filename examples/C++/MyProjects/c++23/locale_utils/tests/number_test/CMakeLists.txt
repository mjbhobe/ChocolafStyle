# ========================================================================================
# NOTE: Although LocaleUtils files require C++ compiler that
# supports C++17 or more, these test files use C++23 standard!
#
# To build targets run the following commands in sequence
#
#   prepare build configs - either debug or release 
#   cmake -S . -B cmake-build-debug -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=clang++
#   OR
#   cmake -S . -B cmake-build-release -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=clang++
#
#   run build
#   cmake --build cmake-build-debug --target number_testX && ./cmake-build-debug/number_testX
#   OR
#   cmake --build cmake-build-release --target number_testX && ./cmake-build-release/number_testX
#
# Author: Manish Bhobe
# My experiments with C/C++, STL and Qt Framework
# Code shared for learning purposes only! Use at your own risk.
# ========================================================================================


cmake_minimum_required(VERSION 3.24)
project(number_test3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ICU REQUIRED icu-i18n icu-uc)
find_package(nlohmann_json REQUIRED)

# ----------------------------------------------
# read/write large numbers with default locale
# ----------------------------------------------
add_executable(number_test1    
    number_test1.cpp
    ../../locale_utils.cpp
)

target_include_directories(number_test1 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(number_test1 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)


# ----------------------------------------------
# read/write large numbers with default locale
# ----------------------------------------------
add_executable(number_test2    
    number_test2.cpp
    ../../locale_utils.cpp
)

target_include_directories(number_test2 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(number_test2 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)

# ----------------------------------------------
# parse/display numbers in locale format
# ----------------------------------------------
add_executable(number_test3
    number_test3.cpp
    ../../locale_utils.cpp
)

target_include_directories(number_test3 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(number_test3 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)

# ----------------------------------------------
# number to text spellout
# ----------------------------------------------
add_executable(number_test4
    number_test4.cpp
    ../../locale_utils.cpp
)

target_include_directories(number_test4 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(number_test4 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)
