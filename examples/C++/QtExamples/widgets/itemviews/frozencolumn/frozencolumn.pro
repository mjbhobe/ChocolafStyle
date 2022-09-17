TEMPLATE = app
TARGET = frozenColumn
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(tableview))

HEADERS += freezetablewidget.h
SOURCES += main.cpp freezetablewidget.cpp
RESOURCES += grades.qrc

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/frozencolumn
INSTALLS += target
