# common.cmake
#
# Global settings file for compiler/linker/includes etc.
# This file DOES NOT build anything; it defines an INTERFACE target that
# exports compile options/defines, include paths and link libs for consumers.

cmake_minimum_required(VERSION 3.21)

# --- Choose C++ standard (qmake had c++20 in CONFIG but also forced -std=c++23)
# Pick 23 to match QMAKE_CXXFLAGS; change to 20 if needed.
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# --- Enable Qt's auto tools globally (mimics qmake's moc/uic/rcc handling)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# ---------------------------------------------------------------------------
# Qt components (from: QT += core gui xml sql network svg; +widgets if Qt>=5)
# ---------------------------------------------------------------------------
# Try Qt6 first, then Qt5, with the listed components.
# find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Gui Xml Sql Network Svg Widgets)
find_package(QT NAMES Qt6 REQUIRED COMPONENTS Core Gui Xml Sql Network Svg Widgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Gui Xml Sql Network Svg Widgets)

# ---------------------------------------------------------------------------
# Interface target that carries all usage requirements
# ---------------------------------------------------------------------------
add_library(chocolaf_settings INTERFACE)

# ---------------------------------------------------------------------------
# Global compile definitions (from DEFINES += ...)
# ---------------------------------------------------------------------------
# Warn on using deprecated Qt APIs
target_compile_definitions(chocolaf_settings INTERFACE QT_DEPRECATED_WARNINGS)

# Disable qDebug() output in Release (from: CONFIG(release): DEFINES += QT_NO_DEBUG_OUTPUT)
target_compile_definitions(chocolaf_settings
  INTERFACE
    $<$<CONFIG:Release>:QT_NO_DEBUG_OUTPUT>
)

# ---------------------------------------------------------------------------
# Per-compiler/per-config compile options (from QMAKE_CXXFLAGS*)
# ---------------------------------------------------------------------------
# -std=c++23 is implied via CMAKE_CXX_STANDARD, but keep the extra warning knobs.
# qmake: -Wno-deprecated-enum-enum-conversion, -pedantic -Wall, O0/O2, g2/g0
target_compile_options(chocolaf_settings
  INTERFACE
    # Common
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wno-deprecated-enum-enum-conversion>
    $<$<CXX_COMPILER_ID:GNU,Clang,AppleClang>:-Wall>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    # Debug
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:GNU,Clang,AppleClang>>:-O0 -g2 -pedantic>
    $<$<AND:$<CONFIG:Debug>,$<CXX_COMPILER_ID:MSVC>>:/Od /Z7>
    # Release
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:GNU,Clang,AppleClang>>:-O2 -g0>
    $<$<AND:$<CONFIG:Release>,$<CXX_COMPILER_ID:MSVC>>:/O2 /Z7-> # strip symbols
)

# ---------------------------------------------------------------------------
# Include paths (from INCLUDEPATH += ...)
# ---------------------------------------------------------------------------
# NOTE: Prefer find_package for real projects; these mimic the original .pro.
target_include_directories(chocolaf_settings
  INTERFACE
    # qmake had: DEPENDPATH+=. INCLUDEPATH+=. and INCLUDEPATH += $$PWD
    ${CMAKE_CURRENT_LIST_DIR}
)

# Platform-specific "COMMON_FILES_HOME" (kept as a variable for consumers)
if(WIN32)
  set(COMMON_FILES_HOME "c:/Dev/Code/git-projects/ChocolafStyle/chocolaf" CACHE PATH "Common files root (Windows)")
else()
  set(COMMON_FILES_HOME "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf" CACHE PATH "Common files root (Unix)")
endif()

# ---------------------------------------------------------------------------
# Optional MSYS2 vs non-MSYS2 Windows toggles (mirrors the qmake branches)
# ---------------------------------------------------------------------------
#option(USE_MSYS2 "Use MSYS2 include/lib layout on Windows" ON) # qmake branch: CONFIG(MSYS2)

if(WIN32)
  if(USE_MSYS2)
    message(STATUS "Using MSYS2 configuration...")
    target_include_directories(chocolaf_settings INTERFACE
      "C:/Dev/msys64/mingw64/include"
      "C:/Dev/msys64/mingw64/include/opencv4"
      "C:/Dev/GNULibs/fmt/bin/include"
    )
    # Library search hints (prefer find_package; these mirror -L entries)
    # If you must use -L, you can set CMAKE_<LANG>_STANDARD_LIBRARIES or link_directories,
    # but target-specific absolute libs are safer. We'll keep link_directories minimal:
    link_directories(
      "C:/Dev/msys64/mingw64/lib"
      "C:/Dev/GNULibs/fmt/bin/lib"
      "C:/Dev/GNULibs/libpqxx/bin/lib"
      "C:/Dev/PostgreSQL/15/lib"
    )
    # OpenCV libs (if not found by find_package)
    set(_OPENCV_MANUAL_LIBS
      opencv_core opencv_imgproc opencv_highgui opencv_ml opencv_video
      opencv_features2d opencv_calib3d opencv_objdetect opencv_videoio
      opencv_imgcodecs opencv_flann
    )
  else()
    message(STATUS "**NOT** using MSYS2 configuration...")
    target_include_directories(chocolaf_settings INTERFACE
      "C:/Dev/GNULibs/gmp-6.2.1/bin/include"
      "C:/Dev/OpenCV/build/x86/mingw/install/include"
      "C:/Dev/GNULibs/fmt/bin/include"
      "C:/Dev/GNULibs/libpqxx/bin/include"
      "C:/Dev/PostgreSQL/15/include"
    )
    link_directories(
      "C:/Dev/GNULibs/gmp-6.2.1/bin/lib"
      "C:/Dev/OpenCV/build/x86/mingw/install/x64/mingw/lib"
      "C:/Dev/GNULibs/fmt/bin/lib"
      "C:/Dev/GNULibs/libpqxx/bin/lib"
      "C:/Dev/PostgreSQL/15/lib"
    )
    # Versioned OpenCV 4.5.1 libs per original .pro
    set(_OPENCV_MANUAL_LIBS
      opencv_core451 opencv_imgproc451 opencv_highgui451 opencv_ml451 opencv_video451
      opencv_features2d451 opencv_calib3d451 opencv_objdetect451 opencv_videoio451
      opencv_imgcodecs451 opencv_flann451
    )
  endif()
else() # UNIX
  message(STATUS "Settings for Linux build")
  # include for gmp.h, gmpxx.h and for OpenCV headers
  target_include_directories(chocolaf_settings INTERFACE
    "/usr/local/include"
    "/usr/include/opencv4"
  )
  set(_OPENCV_MANUAL_LIBS
    opencv_core opencv_imgproc opencv_highgui opencv_ml opencv_video
    opencv_features2d opencv_calib3d opencv_objdetect opencv_videoio
    opencv_imgcodecs opencv_flann
  )
endif()

# ---------------------------------------------------------------------------
# Prefer find_package for 3rd party dependencies (recommended)
# ---------------------------------------------------------------------------
# FMT
find_package(fmt QUIET)
if(fmt_FOUND)
  target_link_libraries(chocolaf_settings INTERFACE fmt::fmt)
endif()

# OpenCV (use if available; otherwise fall back to manual lib list above)
find_package(OpenCV QUIET COMPONENTS core imgproc highgui ml video features2d calib3d objdetect videoio imgcodecs flann)
if(OpenCV_FOUND)
  target_include_directories(chocolaf_settings INTERFACE ${OpenCV_INCLUDE_DIRS})
  target_link_libraries(chocolaf_settings INTERFACE ${OpenCV_LIBS})
else()
  # Manual OpenCV link names (as in the .pro) if find_package fails
  target_link_libraries(chocolaf_settings INTERFACE ${_OPENCV_MANUAL_LIBS})
endif()

# PostgreSQL / libpq
find_package(PostgreSQL QUIET)
if(PostgreSQL_FOUND)
  target_include_directories(chocolaf_settings INTERFACE ${PostgreSQL_INCLUDE_DIRS})
  target_link_libraries(chocolaf_settings INTERFACE ${PostgreSQL_LIBRARIES})
endif()

# libpqxx (no standard CMake package in many distros; link by name if available)
# You may set PQXX_ROOT or rely on link_directories above.
find_library(PQXX_LIBRARY NAMES pqxx)
if(PQXX_LIBRARY)
  target_link_libraries(chocolaf_settings INTERFACE ${PQXX_LIBRARY})
endif()

# GMP (gmp, gmpxx)
find_library(GMP_LIBRARY   NAMES gmp)
find_library(GMPXX_LIBRARY NAMES gmpxx)
if(GMP_LIBRARY)
  target_link_libraries(chocolaf_settings INTERFACE ${GMP_LIBRARY})
endif()
if(GMPXX_LIBRARY)
  target_link_libraries(chocolaf_settings INTERFACE ${GMPXX_LIBRARY})
endif()

# ---------------------------------------------------------------------------
# System libs (from: LIBS += -lUser32 -lGdi32 -lKernel32 -lDwmapi -lShcore, etc.)
# ---------------------------------------------------------------------------
if(WIN32)
  target_link_libraries(chocolaf_settings INTERFACE
    user32 gdi32 kernel32 dwmapi shcore ws2_32 wsock32
  )
else()
  # qmake had: -lm -lstdc++ part of STD_LIBS on *nix
  # Link to m where needed; libstdc++ is implicit when using g++/clang++
  target_link_libraries(chocolaf_settings INTERFACE m)
endif()

# ---------------------------------------------------------------------------
# Link Qt to the interface so consumers get it
# ---------------------------------------------------------------------------
target_link_libraries(chocolaf_settings
  INTERFACE
    Qt${QT_VERSION_MAJOR}::Core
    Qt${QT_VERSION_MAJOR}::Gui
    Qt${QT_VERSION_MAJOR}::Xml
    Qt${QT_VERSION_MAJOR}::Sql
    Qt${QT_VERSION_MAJOR}::Network
    Qt${QT_VERSION_MAJOR}::Svg
    Qt${QT_VERSION_MAJOR}::Widgets
)

# ---------------------------------------------------------------------------
# Sources/Headers/Resources lists (from SOURCES +=, HEADERS +=, RESOURCES +=)
# NOTE: We expose these as variables for consumers to add to their targets.
# ---------------------------------------------------------------------------
set(CHOCOLAF_COMMON_SOURCES
  "${CMAKE_CURRENT_LIST_DIR}/common_funcs.cpp"
  "${CMAKE_CURRENT_LIST_DIR}/chocolaf.cpp"
  CACHE INTERNAL "Common sources to be added by consumers"
)
set(CHOCOLAF_COMMON_HEADERS
  "${CMAKE_CURRENT_LIST_DIR}/common_funcs.h"
  "${CMAKE_CURRENT_LIST_DIR}/chocolaf.h"
  "${CMAKE_CURRENT_LIST_DIR}/argparse/argparse.hpp"
  "${CMAKE_CURRENT_LIST_DIR}/rapidcsv.h"
  CACHE INTERNAL "Common headers to be added by consumers"
)
# qmake: RESOURCES += $$PWD/../styles/chocolaf/chocolaf.qrc
set(CHOCOLAF_QT_RESOURCES
  "${CMAKE_CURRENT_LIST_DIR}/../styles/chocolaf/chocolaf.qrc"
  CACHE INTERNAL "Qt .qrc files for consumers"
)

# If you want these files to show up in IDEs when linking the interface target,
# you can expose them as INTERFACE sources (no compilation is triggered here).
#target_sources(chocolaf_settings INTERFACE
#  ${CHOCOLAF_COMMON_SOURCES}
#  ${CHOCOLAF_COMMON_HEADERS}
#  ${CHOCOLAF_QT_RESOURCES}
#)

# Consumers using Qt6 can also do: qt_add_resources(<target> ... ${CHOCOLAF_QT_RESOURCES})

# ---------------------------------------------------------------------------
# QtAwesome (qmake: CONFIG += fontAwesomeFree; include(QtAwesome/QtAwesome.pri))
# ---------------------------------------------------------------------------

# ---- QtAwesome (vendored sources beside this file) ---------------------------
# Turn on/off globally
option(ENABLE_QTAWESOME "Build and link QtAwesome icon helper" ON)

if(ENABLE_QTAWESOME)
  # Path: QtAwesome is a sibling of this common.cmake file
  set(QTAWESOME_ROOT "${CMAKE_CURRENT_LIST_DIR}/QtAwesome")

  if(EXISTS "${QTAWESOME_ROOT}/QtAwesome.cpp")
#    add_library(QtAwesome STATIC
#        "${QTAWESOME_ROOT}/QtAwesome.cpp"
#        "${QTAWESOME_ROOT}/QtAwesome.h"
#        "${QTAWESOME_ROOT}/QtAwesomeAnim.cpp"
#        "${QTAWESOME_ROOT}/QtAwesomeAnim.h"
#    )
    #target_include_directories(QtAwesome PUBLIC "${QTAWESOME_ROOT}")
    target_include_directories(chocolaf_settings INTERFACE "${QTAWESOME_ROOT}")
    # append QtAwesome header files to includes list
    list(APPEND CHOCOLAF_COMMON_HEADERS "${QTAWESOME_ROOT}/QtAwesome.h")
    list(APPEND CHOCOLAF_COMMON_HEADERS "${QTAWESOME_ROOT}/QtAwesomeAnim.h")
    set(CHOCOLAF_COMMON_HEADERS
      "${CHOCOLAF_COMMON_HEADERS}"
      CACHE INTERNAL "Common sources to be added by consumers" FORCE)

    # # append QtAwesome source files to sources list
    list(APPEND CHOCOLAF_COMMON_SOURCES "${QTAWESOME_ROOT}/QtAwesome.cpp")
    list(APPEND CHOCOLAF_COMMON_SOURCES "${QTAWESOME_ROOT}/QtAwesomeAnim.cpp")
    set(CHOCOLAF_COMMON_SOURCES
        "${CHOCOLAF_COMMON_SOURCES}"
        CACHE INTERNAL "Common sources to be added by consumers" FORCE)

#    target_link_libraries(QtAwesome PUBLIC
#        Qt${QT_VERSION_MAJOR}::Core
#        Qt${QT_VERSION_MAJOR}::Gui
#        Qt${QT_VERSION_MAJOR}::Widgets
#    )

    # If the repo (or you) provide a .qrc with Font Awesome fonts, add it here:
    if(EXISTS "${QTAWESOME_ROOT}/QtAwesomeFree.qrc")
      # AUTORCC is already ON globally; adding the .qrc is enough
      #target_sources(QtAwesome PRIVATE "${QTAWESOME_ROOT}/QtAwesome.qrc")

      list(APPEND CHOCOLAF_QT_RESOURCES "${QTAWESOME_ROOT}/QtAwesomeFree.qrc")
      set(CHOCOLAF_QT_RESOURCES
          "${CMAKE_CURRENT_LIST_DIR}/../styles/chocolaf/chocolaf.qrc"
          CACHE INTERNAL "Qt .qrc files for consumers" FORCE
      )
    endif()

    # Make all consumers of chocolaf_settings get QtAwesome automatically
    # target_link_libraries(chocolaf_settings INTERFACE QtAwesome)
    message(STATUS "QtAwesome enabled from: ${QTAWESOME_ROOT}")
  else()
    message(WARNING "QtAwesome not found at ${QTAWESOME_ROOT}. Set ENABLE_QTAWESOME=OFF or place sources there.")
  endif()
endif()
# --------------------------------------------------------------------------
# Output directories (qmake DESTDIR/build/debug|release)
# NOTE: CMake defaults differ; set global dirs to mimic qmake layout.
# ---------------------------------------------------------------------------
# Use ${CMAKE_BINARY_DIR}/build/<config> to separate artifacts
set(_out_base "${CMAKE_BINARY_DIR}/build")
foreach(_cfg Debug Release RelWithDebInfo MinSizeRel)
  string(TOUPPER "${_cfg}" _CFG)
  set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_${_CFG} "${_out_base}/${_cfg}")
  set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_${_CFG} "${_out_base}/${_cfg}")
  set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY_${_CFG} "${_out_base}/${_cfg}")
endforeach()


# If you want these files to show up in IDEs when linking the interface target,
# you can expose them as INTERFACE sources (no compilation is triggered here).
target_sources(chocolaf_settings INTERFACE
    ${CHOCOLAF_COMMON_SOURCES}
    ${CHOCOLAF_COMMON_HEADERS}
    ${CHOCOLAF_QT_RESOURCES}
)

# qmake also set OBJECTS_DIR/MOC_DIR/RCC_DIR/UI_DIR under DESTDIR.
# CMake manages moc/rcc/uic in its own build tree; overriding their
# directories is uncommon and generally unnecessary, so we omit that here.
# ---------------------------------------------------------------------------

# How to consume this in your CMake project:
#
#   include(${CMAKE_SOURCE_DIR}/cmake/ChocolafGlobal.cmake)
#   add_executable(myapp main.cpp)
#   target_link_libraries(myapp PRIVATE chocolaf_settings)
#   target_sources(myapp PRIVATE ${CHOCOLAF_COMMON_SOURCES} ${CHOCOLAF_QT_RESOURCES})
#   target_include_directories(myapp PRIVATE ${CHOCOLAF_COMMON_HEADERS}) # headers are header-only
#
# If OpenCV/fmt/PostgreSQL/libpqxx aren’t auto-found, either:
#  - set USE_MSYS2 ON and keep the link_directories/include dirs above, or
#  - provide CMAKE_PREFIX_PATH / *_ROOT hints to their installations.

# --- Debug summary for chocolaf_settings ------------------------------------

# 1. Include directories
get_target_property(_choco_includes chocolaf_settings INTERFACE_INCLUDE_DIRECTORIES)

# 2. Linked libraries
get_target_property(_choco_libs chocolaf_settings INTERFACE_LINK_LIBRARIES)

# 3. Search paths (used by link_directories() etc.)
get_directory_property(_link_dirs DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} LINK_DIRECTORIES)

# 4. Common headers (includes appended ones like QtAwesome.h)
set(_choco_headers "${CHOCOLAF_COMMON_HEADERS}")

# 5. Common sources (includes appended ones like QtAwesome.cpp)
set(_choco_sources "${CHOCOLAF_COMMON_SOURCES}")

# 6. Common resources (all *.qrc files)
set(_choco_resources "${CHOCOLAF_QT_RESOURCES}")

# Flatten for pretty-printing
string(REPLACE ";" "\n    " _includes_str "${_choco_includes}")
string(REPLACE ";" "\n    " _libs_str     "${_choco_libs}")
string(REPLACE ";" "\n    " _choco_headers_str "${_choco_headers}")
string(REPLACE ";" "\n    " _choco_sources_str "${_choco_sources}")
string(REPLACE ";" "\n    " _choco_resources_str "${_choco_resources}")

message(STATUS "====== Chocolaf Common Settings ======")
message(STATUS "Include dirs:\n    ${_includes_str}")
message(STATUS "Library search paths:\n    ${_linkdirs_str}")
message(STATUS "Linked libs:\n    ${_libs_str}")
message(STATUS "Common includes:\n    ${_choco_headers_str}")
message(STATUS "Common sources:\n    ${_choco_sources_str}")
message(STATUS "Common resources:\n    ${_choco_resources_str}")
message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
message(STATUS "CMAKE_LIBRARY_PATH: ${CMAKE_LIBRARY_PATH}")
message(STATUS "CMAKE_INCLUDE_PATH: ${CMAKE_INCLUDE_PATH}")
message(STATUS "======================================")



