TEMPLATE = app
TARGET = first
INCLUDEPATH += .

# include (../../../../../chocolaf/common_files/common.pro)
include ($$(CHOCOLAF_HOME)/chocolaf/common_files/common.pro)

SOURCES += \
    Window.cpp \
    main.cpp

HEADERS += \
    Window.h

