TEMPLATE = app
TARGET = notepad
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)

qtHaveModule(printsupport): QT += printsupport
#requires(qtConfig(fontdialog))

SOURCES += \
    main.cpp\
    notepad.cpp

HEADERS += notepad.h

FORMS += notepad.ui

RESOURCES += \
    notepad.qrc

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/tutorials/notepad
INSTALLS += target
