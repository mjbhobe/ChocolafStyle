// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include "chocolaf.h"
#include "window.h"
#include <QApplication>

int main(int argc, char* argv[])
{
    // QApplication app(argc, argv);
#ifdef Q_OS_WIN
    // set dark mode on Windows
    // @see: https://www.qt.io/blog/dark-mode-on-windows-11-with-qt-6.5
    qputenv("QT_QPA_PLATFORM", "windows:darkmode=2");
#endif
    Chocolaf::ChocolafApp::setupForHighDpiScreens();
    Chocolaf::ChocolafApp app(argc, argv);
    app.setStyle("Fusion");

    Window window;
    window.show();
    return app.exec();
}
