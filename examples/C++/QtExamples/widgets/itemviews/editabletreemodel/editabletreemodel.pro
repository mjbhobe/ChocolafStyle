TEMPLATE = app
TARGET = editableTreeModel
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(treeview))

FORMS       += mainwindow.ui
HEADERS     += mainwindow.h \
              treeitem.h \
              treemodel.h
RESOURCES   += editabletreemodel.qrc
SOURCES     += mainwindow.cpp \
              treeitem.cpp \
              treemodel.cpp \
              main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/editabletreemodel
INSTALLS += target
