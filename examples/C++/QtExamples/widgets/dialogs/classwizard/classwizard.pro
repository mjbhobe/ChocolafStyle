TEMPLATE = app
TARGET = classwizard

include (../../../../../../chocolaf/common_files/common.pro)

HEADERS       += classwizard.h
SOURCES       += classwizard.cpp \
                main.cpp
RESOURCES     += classwizard.qrc

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/dialogs/classwizard
INSTALLS += target
