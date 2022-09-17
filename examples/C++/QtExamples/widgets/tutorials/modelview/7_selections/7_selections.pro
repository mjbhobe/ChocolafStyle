TARGET = mv_selections
TEMPLATE = app
INCLUDEPATH += .
include(../../../../../../../chocolaf/common_files/common.pro)
#requires(qtConfig(treeview))

SOURCES += main.cpp \
    mainwindow.cpp
HEADERS += mainwindow.h

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/modelview/7_selections
INSTALLS += target
