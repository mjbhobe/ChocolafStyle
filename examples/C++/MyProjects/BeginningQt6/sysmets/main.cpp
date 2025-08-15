// -------------------------------------------------------------------------------
// main.cpp: main driver program
//
// Sysmets - Windows System Metrics as shown in the book
// Programming Windows by Charles Petzold (Microsoft Press)
// We use a QTableView, so data shows up in a grid, with auto scrolling!
//
// Author: Manish Bhobe
// My Experiments with C/C++ and QT Framework
// Code is meant for illustration only! Use at your own risk. Author is not
// liable for any direct/indirect damage caused due to use of this code.
// -------------------------------------------------------------------------------
#include "SysmetsModel.h"
#include "chocolaf.h"
#include "sysmets.h"

#include <QApplication>
#include <QMainWindow>
#include <QMessageBox>
#include <QTableView>

// NOTE: this code is for Windows only!
#ifndef Q_OS_WIN
// Code for other operating systems (Mac, Linux, etc.)
QMessageBox::critical(nullptr, "Error", "This program is designed to run only on Windows.");
return 1; // Exit with an error code
#endif

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  //app.setStyle("Fusion");
  //Chocolaf::setChocolafStyle(app, "Fusion");

  // create & show main GUI
  SysmetsModel model;
  QTableView tableView;
  tableView.setModel(&model);
  tableView.resizeColumnsToContents();
  // tableView.show();

  QMainWindow mainWindow;
  mainWindow.resize(400, 250);
  mainWindow.setWindowTitle("Windows System Metrics with Qt");
  mainWindow.setCentralWidget(&tableView);
  mainWindow.show();

  return app.exec();
}
