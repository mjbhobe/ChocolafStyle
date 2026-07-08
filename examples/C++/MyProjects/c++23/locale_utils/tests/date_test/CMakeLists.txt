cmake_minimum_required(VERSION 3.24)
project(date_test3 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ICU REQUIRED icu-i18n icu-uc)
find_package(nlohmann_json REQUIRED)

# ----------------------------------------------
# round-trip: format_short_date_time() -> parse_date_time(), plus
# rejection of impossible/partial input
# ----------------------------------------------
add_executable(date_test3
    date_test3.cpp
    ../../locale_utils.cpp
)

target_include_directories(date_test3 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(date_test3 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)

# ----------------------------------------------
# four locales, one code path: format/parse dates and date-times
# ----------------------------------------------
add_executable(date_test4
    date_test4.cpp
    ../../locale_utils.cpp
)

target_include_directories(date_test4 PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(date_test4 PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)

# ----------------------------------------------
# calendar/era gotcha: ja_JP default (Gregorian) vs
# ja_JP@calendar=japanese (imperial era)
# ----------------------------------------------
add_executable(date_test_calendar
    date_test_calendar.cpp
    ../../locale_utils.cpp
)

target_include_directories(date_test_calendar PRIVATE ${ICU_INCLUDE_DIRS} ../..)
target_link_libraries(date_test_calendar PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)
