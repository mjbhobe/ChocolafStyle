TEMPLATE = app
TARGET = addressBook

include (../../../../../../chocolaf/common_files/common.pro)

SOURCES += main.cpp listDialog.cpp editDialog.cpp
HEADERS += listDialog.h editDialog.h
FORMS += listDialog.ui editDialog.ui

