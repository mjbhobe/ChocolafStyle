TEMPLATE = app
TARGET = graphicsview

include (../../../../../../chocolaf/common_files/common.pro)

SOURCES += main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/scroller/graphicsview
INSTALLS += target
