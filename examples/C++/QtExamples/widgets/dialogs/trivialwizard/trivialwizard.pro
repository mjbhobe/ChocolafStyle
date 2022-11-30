TEMPLATE = app
TARGET = trivialwizard

include (../../../../../../chocolaf/common_files/common.pro)

SOURCES       += trivialwizard.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/dialogs/trivialwizard
INSTALLS += target
