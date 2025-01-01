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
#include <QTableView>

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
  mainWindow.setWindowTitle("Windows System Metrics with Qt");
  mainWindow.setCentralWidget(&tableView);
  mainWindow.show();

  return app.exec();
}
