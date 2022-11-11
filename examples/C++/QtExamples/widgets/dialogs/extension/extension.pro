TEMPLATE = app
TARGET = extension

include (../../../../../../chocolaf/common_files/common.pro)

HEADERS       += finddialog.h
SOURCES       += finddialog.cpp \
                main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/dialogs/extension
INSTALLS += target
