QT += widgets
TEMPLATE = app
TARGET = part7
INCLUDEPATH += .

include(../../../../../../../chocolaf/common_files/common.pro)

requires(qtConfig(filedialog))

SOURCES   = addressbook.cpp \
            finddialog.cpp \
            main.cpp
HEADERS   = addressbook.h \
            finddialog.h

QMAKE_PROJECT_NAME = ab_part7

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/addressbook/part7
INSTALLS += target
