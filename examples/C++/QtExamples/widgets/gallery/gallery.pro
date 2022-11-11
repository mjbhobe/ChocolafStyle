TEMPLATE = app
TARGET = gallery

include (../../../../../chocolaf/common_files/common.pro)

HEADERS       += widgetgallery.h
SOURCES       += main.cpp \
                widgetgallery.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/gallery
INSTALLS += target
