cmake_minimum_required(VERSION 3.24)
project(number_test3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ICU REQUIRED icu-i18n icu-uc)
find_package(nlohmann_json REQUIRED)

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
