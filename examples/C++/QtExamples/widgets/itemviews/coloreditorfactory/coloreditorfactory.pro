TEMPLATE = app
TARGET = coloreditorfactory
INCLUDEPATH += .
include(../../../../../../chocolaf/common_files/common.pro)
requires(qtConfig(combobox))

HEADERS	 += colorlisteditor.h \
	      	window.h
SOURCES	 += colorlisteditor.cpp \
	      	window.cpp \
	      	main.cpp

# install
target.path = $$[QT_INSTALL_EXAMPLES]/widgets/itemviews/coloreditorfactory
INSTALLS += target
