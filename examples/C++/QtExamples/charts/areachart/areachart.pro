TEMPLATE = app
TARGET = areachart
INCLUDEPATH += .
include(../../../../../chocolaf/common_files/common.pro)
QT += charts

SOURCES += \
    main.cpp

target.path = $$[QT_INSTALL_EXAMPLES]/charts/areachart
INSTALLS += target
