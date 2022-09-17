TEMPLATE = app
TARGET = flatTreeView
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)

SOURCES     += main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/flattreeview
INSTALLS += target
