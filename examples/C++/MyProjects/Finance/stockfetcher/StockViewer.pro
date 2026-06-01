TARGET=StockViewer
QT += core gui widgets

CONFIG += c++23

SOURCES += main.cpp \
           MainWindow.cpp \
           DataFetcher.cpp \
           StockModel.cpp

HEADERS += MainWindow.h \
           DataFetcher.h \
           StockModel.h

# Windows Configuration (MSYS2 Environment Paths Setup)
win32 {
    INCLUDEPATH += C:/msys64/mingw64/include
    LIBS += -LC:/msys64/mingw64/lib -lcurl
}

# Linux Configuration (Manjaro)
unix:!macx {
    LIBS += -lcurl
}
