TEMPLATE = app
TARGET = barmodelmapper
QT += charts
requires(qtConfig(tableview))
include(../../../../../chocolaf/common_files/common.pro)

HEADERS += \
    customtablemodel.h \
    tablewidget.h

SOURCES += \
    customtablemodel.cpp \
    main.cpp \
    tablewidget.cpp

target.path = $$[QT_INSTALL_EXAMPLES]/charts/barmodelmapper
INSTALLS += target
