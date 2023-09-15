// ============================================================================
// step08.cc: Loading & saving collection of lines
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
// Created by Manish Bhobe.
// ===========================================================================

#include "MainWindow.h"
#include "chocolaf.h"
#include <QApplication>
#include <QtGui>

const QString AppTitle("Qt Scribble");

int main(int argc, char** argv)
{
    /* Chocolaf::ChocolafApp::setupForHighDpiScreens();
    Chocolaf::ChocolafApp app(argc, argv);
    app.setStyle("Fusion");*/

    QApplication app(argc, argv);
    app.setStyle("Fusion");

    app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

    // create the GUI
    MainWindow mainWindow;
    Chocolaf::centerOnScreenWithSize(mainWindow, 0.75, 0.75);
    // mainWindow.resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
    mainWindow.show();

    return app.exec();
}
