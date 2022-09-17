TEMPLATE = app
TARGET = chart
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(filedialog))

HEADERS     += mainwindow.h \
              pieview.h
RESOURCES   += chart.qrc
SOURCES     += main.cpp \
              mainwindow.cpp \
              pieview.cpp
unix:!mac:!vxworks:!integrity:!haiku:LIBS += -lm

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/chart
INSTALLS += target
