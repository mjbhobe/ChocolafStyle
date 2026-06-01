TARGET=PortfolioViewer
QT += core gui widgets

CONFIG += c++23

SOURCES += main.cpp \
           MainWindow.cpp \
           DataFetcher.cpp \
           PortfolioModel.cpp

HEADERS += MainWindow.h \
           DataFetcher.h \
           PortfolioModel.h

# Windows Configuration (MSYS2 Environment Paths Setup)
win32 {
    INCLUDEPATH += C:/msys64/mingw64/include
    LIBS += -LC:/msys64/mingw64/lib -lcurl
}

# Linux Configuration (Manjaro)
unix:!macx {
    LIBS += -lcurl
}

