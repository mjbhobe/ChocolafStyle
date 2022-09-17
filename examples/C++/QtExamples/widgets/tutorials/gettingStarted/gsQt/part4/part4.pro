
TEMPLATE = app
TARGET = part4
INCLUDEPATH += .

include(../../../../../../../../chocolaf/common_files/common.pro)

SOURCES = main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/gettingStarted/gsQt/part4
INSTALLS += target
