// ch03/spreadsheet/mainwindow.cc
#include "mainwindow.h"
#include "findDialog.h"
#include "gotoCellDialog.h"
#include "spreadsheet.h"
#include <QtGui>

MainWindow::MainWindow()
{
  spreadSheet = new Spreadsheet;
  setCentralWidget(spreadSheet);

  createActions();
  createMenus();
  createContextMenu();
  createToolBars();
  createStatusBar();
  readSettings();
  findDialog = nullptr;

  setWindowIcon(QIcon(":/icons/spreadsheet.png"));
  setCurrentFile("");
}

void MainWindow::createActions()
{
  // TODO
}

void MainWindow::createMenus()
{
  // TODO
}

void MainWindow::createContextMenu()
{
  // TODO
}

void MainWindow::createToolBars()
{
  // TODO
}

void MainWindow::createStatusBar()
{
  // TODO
}

void MainWindow::readSettings()
{
  // TODO
}
