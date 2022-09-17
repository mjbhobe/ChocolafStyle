TEMPLATE = app
TARGET = starDelegate
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(tablewidget))

HEADERS       += stardelegate.h \
                stareditor.h \
                starrating.h
SOURCES       += main.cpp \
                stardelegate.cpp \
                stareditor.cpp \
                starrating.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/stardelegate
INSTALLS += target
