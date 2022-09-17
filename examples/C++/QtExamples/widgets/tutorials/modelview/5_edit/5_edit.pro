TARGET = mv_edit
TEMPLATE = app
INCLUDEPATH += .
include(../../../../../../../chocolaf/common_files/common.pro)
# requires(qtConfig(tableview))

SOURCES += main.cpp \
           mainwindow.cpp \
           mymodel.cpp

HEADERS += mainwindow.h \
           mymodel.h

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/modelview/5_edit
INSTALLS += target
