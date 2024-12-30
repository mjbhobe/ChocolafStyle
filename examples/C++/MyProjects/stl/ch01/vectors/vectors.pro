TEMPLATE = app
TARGET = vec1
CONFIG += console c++20
CONFIG -= app_bundle
CONFIG -= qt
QMAKE_CXXFLAGS += -Wno-c11-extensions -Wno-deprecated-anon-enum-enum-conversion -Wno-unused-variable \
    -Wno-unused-parameter -DCONSOLE_MODE -std=c++20
QMAKE_CXXFLAGS_DEBUG += -O0 -g2 -Wall -pedantic
QMAKE_CXXFLAGS_RELEASE += -O2 -g0 -Wall

SOURCES += \
  vec1.cpp
