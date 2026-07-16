cmake_minimum_required(VERSION 3.20)
project(locale_utils VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(GNUInstallDirs)

find_package(ICU REQUIRED COMPONENTS uc i18n)
find_package(nlohmann_json CONFIG REQUIRED)

add_library(locale_utils SHARED
    locale_utils.cpp
)

target_include_directories(locale_utils
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

target_link_libraries(locale_utils
    PUBLIC
        ICU::uc
        ICU::i18n
        nlohmann_json::nlohmann_json
)

set_target_properties(locale_utils PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 1
    PUBLIC_HEADER locale_utils.h
)

# On Linux/macOS the install location is a stable, compiled-in path (the
# FHS convention). Windows has no such convention -- locale_utils.cpp
# resolves the DLL's own directory at runtime instead, so no baked path
# is needed there.
if(NOT WIN32)
    target_compile_definitions(locale_utils PRIVATE
        LOCALE_UTILS_DATA_DIR="${CMAKE_INSTALL_FULL_DATADIR}/locale_utils")
endif()

install(TARGETS locale_utils
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(FILES locales_config.json
    DESTINATION ${CMAKE_INSTALL_DATADIR}/locale_utils
)
