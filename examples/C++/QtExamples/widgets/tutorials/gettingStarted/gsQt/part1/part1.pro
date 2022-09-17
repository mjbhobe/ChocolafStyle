
TEMPLATE = app
TARGET = part1
INCLUDEPATH += .

include(../../../../../../../../chocolaf/common_files/common.pro)


SOURCES = main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/gettingStarted/gsQt/part1
INSTALLS += target
