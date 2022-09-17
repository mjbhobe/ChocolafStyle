TARGET = windowlayout
TEMPLATE = app
INCLUDEPATH += .
include(../../../../../../../chocolaf/common_files/common.pro)

SOURCES += main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/widgets/windowlayout
INSTALLS += target
