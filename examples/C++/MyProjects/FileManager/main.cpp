// main.cpp
// Entry point for QtFileManager
// C++20 | Qt6 Widgets

#include <QApplication>
#include <QStyleFactory>
#include "MainWindow.h"

int main(int argc, char* argv[])
{
    // High-DPI scaling is automatic in Qt6 — no manual setAttribute needed.
    QApplication app(argc, argv);

    app.setApplicationName(QStringLiteral("QtFileManager"));
    app.setApplicationVersion(QStringLiteral("0.1.0"));
    app.setOrganizationName(QStringLiteral("QtFileManagerProject"));

    MainWindow window;
    window.show();

    return app.exec();
}
