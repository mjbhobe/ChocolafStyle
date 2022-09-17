TEMPLATE = app
TARGET = dirView
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(treeview))

SOURCES       += main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/dirview
INSTALLS += target
