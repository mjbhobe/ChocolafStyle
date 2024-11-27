TEMPLATE = app
CONFIG += console c++20
CONFIG -= app_bundle
TARGET = loadImage

include ($$(CHOCOLAF_HOME)/chocolaf/common_files/common_console.pro)

SOURCES += \
        main.cpp
