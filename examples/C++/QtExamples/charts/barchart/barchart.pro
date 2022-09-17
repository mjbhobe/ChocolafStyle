TEMPLATE = app
TARGET = barchart
INCLUDEPATH += .
include(../../../../../chocolaf/common_files/common.pro)
QT += charts

SOURCES += \
    main.cpp

target.path = $$[QT_INSTALL_EXAMPLES]/charts/barchart
INSTALLS += target
