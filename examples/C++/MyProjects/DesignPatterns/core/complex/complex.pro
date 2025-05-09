TEMPLATE = app
TARGET = complex
INCLUDEPATH += .

CONFIG += c++17 console
CONFIG -= app_bundle

#include (../../../../../../chocolaf/common_files/common_console.pro)
include ($$(CHOCOLAF_COMMONFILES_HOME)/common_console.pro)

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        main.cpp \
        complex.cpp

HEADERS += \
        complex.h

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
