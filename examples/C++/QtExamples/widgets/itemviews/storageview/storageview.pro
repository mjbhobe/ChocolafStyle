TEMPLATE = app
TARGET = storageview
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(treeview))

SOURCES += storagemodel.cpp \
    main.cpp
HEADERS += \
    storagemodel.h

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/storageview
INSTALLS += target
