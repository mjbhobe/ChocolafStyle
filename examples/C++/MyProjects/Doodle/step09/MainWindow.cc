// MainWindow.cc: implements MainWindow class
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

#include "MainWindow.h"
#include "DrawWindow.h"
#include "chocolaf.h"
#include "constants.h"
#include "IconFont.h"

MainWindow::MainWindow(QWidget* parent/*=nullptr*/)
  : QMainWindow(parent)
{
  _drawWindow = new DrawWindow();
  setWindowIcon(QIcon(":/icons/appIcon.png"));

  createActions();
  createMenus();
  createToolbar();
  statusBar()->showMessage(
    QString("%1 - Doodling Application by %2. Created by Manish Bhobé").arg(
      QApplication::instance()->applicationName()
    ).arg(QApplication::instance()->organizationName())
  );

  setCentralWidget(_drawWindow);
  resize(QGuiApplication::primaryScreen()->availableSize() * 3 / 5);
}

void MainWindow::createActions()
{
  Q_ASSERT(_drawWindow != 0);

  // get recommended icon dimension for screen DPI
  int iconDim = IconFont::getRecommendedToolbarIconSize(this).width();

  //fileNewAction = new QAction(QIcon(":/icons/fileNew.png"), tr("&New"), this);
  fileNewAction = new QAction(tr("&New"), this);
  fileNewAction->setIcon(IconFont::getIcon(IconFont::Icons::FileNew, iconDim));
  fileNewAction->setShortcut(tr("Ctrl+N"));
  fileNewAction->setStatusTip(tr("Create a new scribble document."));
  QObject::connect(fileNewAction, SIGNAL(triggered()), _drawWindow, SLOT(fileNew()));

  // fileOpenAction = new QAction(QIcon(":/icons/fileOpen.png"), tr("&Open..."), this);
  fileOpenAction = new QAction(tr("&Open..."), this);
  fileOpenAction->setIcon(IconFont::getIcon(IconFont::Icons::FileOpen, iconDim));
  fileOpenAction->setShortcut(tr("Ctrl+O"));
  fileOpenAction->setStatusTip(tr("Open scribble document from disk file."));
  QObject::connect(fileOpenAction, SIGNAL(triggered()), _drawWindow, SLOT(fileOpen()));

  //fileSaveAction = new QAction(QIcon(":/icons/fileSave.png"), tr("&Save"), this);
  fileSaveAction = new QAction(tr("&Save"), this);
  fileSaveAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSave, iconDim));
  fileSaveAction->setShortcut(tr("Ctrl+S"));
  fileSaveAction->setStatusTip(tr("Save scribble document to disk file."));
  QObject::connect(fileSaveAction, SIGNAL(triggered()), _drawWindow, SLOT(fileSave()));

  //fileSaveAsAction = new QAction(QIcon(":/icons/fileSaveAs.png"), tr("Save &as..."), this);
  fileSaveAsAction = new QAction(tr("Save &as..."), this);
  fileSaveAsAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSaveAs, iconDim));
  fileSaveAsAction->setStatusTip(tr("Save scribble document to disk with different name."));
  QObject::connect(fileSaveAsAction, SIGNAL(triggered()), _drawWindow, SLOT(fileSaveAs()));

  exitAction = new QAction(tr("E&xit"), this);
  exitAction->setStatusTip(tr("Save all pending changes and quit application."));
  QObject::connect(exitAction, SIGNAL(triggered()), this, SLOT(exitApp()));

  // penWidthAction = new QAction(
  //   QIcon(":/icons/penWidth.png"), tr("Change pen &width..."), this
  // );
  penWidthAction = new QAction(tr("Change pen &width..."), this);
  penWidthAction->setIcon(IconFont::getIcon(IconFont::Icons::LineWeight, iconDim));
  penWidthAction->setStatusTip(tr("Change the width of default pen."));
  QObject::connect(penWidthAction, SIGNAL(triggered()), _drawWindow, SLOT(changePenWidth()));

  // penColorAction = new QAction(
  //   QIcon(":/icons/penColor.png"), tr("Change pen &color..."), this
  // );
  penColorAction = new QAction(tr("Change pen &color..."), this);
  penColorAction->setIcon(IconFont::getIcon(IconFont::Icons::ColorLens, iconDim));
  penColorAction->setStatusTip(tr("Change the color of default pen."));
  QObject::connect(penColorAction, SIGNAL(triggered()), _drawWindow, SLOT(changePenColor()));

  aboutQtAction = new QAction(tr("&About Qt..."), this);
  aboutQtAction->setStatusTip(tr("Display information Qt Library used."));
  QObject::connect(aboutQtAction, SIGNAL(triggered()), qApp, SLOT(aboutQt()));

  aboutAction = new QAction(tr("&About..."), this);
  aboutAction->setStatusTip(tr("Display information about program."));
  QObject::connect(aboutAction, SIGNAL(triggered()), this, SLOT(about()));
}

void MainWindow::createMenus()
{
  fileMenu = new QMenu(tr("&File"), this);
  fileMenu->addAction(fileNewAction);
  fileMenu->addAction(fileOpenAction);
  fileMenu->addAction(fileSaveAction);
  fileMenu->addAction(fileSaveAsAction);
  fileMenu->addSeparator();
  fileMenu->addAction(exitAction);

  optionsMenu = new QMenu(tr("&Options"), this);
  optionsMenu->addAction(penWidthAction);
  optionsMenu->addAction(penColorAction);

  helpMenu = new QMenu(tr("&Help"), this);
  helpMenu->addAction(aboutAction);
  helpMenu->addAction(aboutQtAction);

  menuBar()->addMenu(fileMenu);
  menuBar()->addMenu(optionsMenu);
  menuBar()->addMenu(helpMenu);
}

void MainWindow::createToolbar()
{
  QToolBar* toolBar = new QToolBar("Main", this);

  // Set the toolbar to display larger icons matching high-DPI scaling
  toolBar->setIconSize(IconFont::getRecommendedToolbarIconSize(this));

  toolBar->addAction(fileNewAction);
  toolBar->addAction(fileOpenAction);
  toolBar->addAction(fileSaveAction);
  toolBar->addAction(fileSaveAsAction);
  toolBar->addSeparator();
  toolBar->addAction(penWidthAction);
  toolBar->addAction(penColorAction);
  addToolBar(toolBar);
}

void MainWindow::exitApp()
{
  close();
}

void MainWindow::about()
{
  QString str = QString(
    "<html><b>Qt Scribble</b> - Doodling application<p/>Developed with the Qt "
    "%1 C++ framework.<p/><p/>Written by - %2.<p/>" "Copyright(C) %3<p/>"
    "<small>Program developed for illustration purposes only! Use at your own  "
    "risk! Author is not responsible for any damages (direct or indirect) that "
    "may result from the use of this program.</small></html>"
  ).arg(QT_VERSION_STR).arg(Chocolaf::__author__).arg(Chocolaf::__organization__);
  QMessageBox::about(this, AppTitle, str);
}
