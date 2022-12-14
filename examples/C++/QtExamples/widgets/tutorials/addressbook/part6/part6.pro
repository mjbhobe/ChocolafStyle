TEMPLATE = app
TARGET = part6
INCLUDEPATH += .

include(../../../../../../../chocolaf/common_files/common.pro)

requires(qtConfig(filedialog))

SOURCES   = addressbook.cpp \
            finddialog.cpp \
            main.cpp
HEADERS   = addressbook.h \
            finddialog.h

QMAKE_PROJECT_NAME = ab_part6

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/addressbook/part6
INSTALLS += target
