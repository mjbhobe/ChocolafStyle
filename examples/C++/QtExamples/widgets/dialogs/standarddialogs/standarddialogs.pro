TEMPLATE = app
TARGET = standarddialogs

include (../../../../../../chocolaf/common_files/common.pro)

HEADERS       += dialog.h
SOURCES       += dialog.cpp \
                main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/dialogs/standarddialogs
INSTALLS += target
