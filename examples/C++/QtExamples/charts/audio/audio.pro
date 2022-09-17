TEMPLATE = app
TARGET = audio
INCLUDEPATH += .
include(../../../../../chocolaf/common_files/common.pro)

QT += charts multimedia

HEADERS += \
    widget.h \
    xyseriesiodevice.h

SOURCES += \
    main.cpp\
    widget.cpp \
    xyseriesiodevice.cpp

target.path = $$[QT_INSTALL_EXAMPLES]/charts/audio
INSTALLS += target
