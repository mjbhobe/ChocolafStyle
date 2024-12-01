TEMPLATE = app
CONFIG += console c++20
CONFIG -= app_bundle
TARGET = loadImage

include ($$(CHOCOLAF_HOME)/chocolaf/common_files/common_console.pro)
# add custom compiler flags - turn of deprecation warnings on OpenCV
QMAKE_CXXFLAGS += -Wno-deprecated-enum-enum-conversion

SOURCES += \
        main.cpp
