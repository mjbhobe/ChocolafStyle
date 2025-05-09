TEMPLATE = app
TARGET = choco_test

# include (../../../../../chocolaf/common_files/common.pro)
include ($$(CHOCOLAF_HOME)/chocolaf/common_files/common.pro)
CONFIG += c++23
QMAKE_CXX = clang++
QMAKE_CXXFLAGS += -std=c++23
QMAKE_LFLAGS += -std=c++23

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    mainwindow.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
