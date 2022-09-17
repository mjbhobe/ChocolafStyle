TEMPLATE = app
TARGET = basicfiltermodel
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(combobox))

HEADERS     += window.h
SOURCES     += main.cpp \
              window.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/basicsortfiltermodel
INSTALLS += target
