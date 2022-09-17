// MainWindow.cc: implements MainWindow class
#include "MainWindow.h"
#include "DrawWindow.h"
#include "chocolaf.h"
#include <QAction>
#include <QMainWindow>
#include <QMenu>
#include <QMenuBar>
#include <QMessageBox>
#include <QStatusBar>
#include <QTextStream>
#include <QToolBar>

const QString AppTitle("Qt Scribble");
const QString WindowTitle = QString("Qt %1 Doodle - Step09: Building a concious GUI").arg(QT_VERSION_STR);

MainWindow::MainWindow()
{
   setWindowTitle(WindowTitle);
   _drawWindow = new DrawWindow();
   setWindowIcon(QIcon(":/icons/appIcon.png"));

   createActions();
   createMenus();
   createToolBar();
   createStatusBar();
   statusBar()->showMessage(QString("%1 - Doodling Application by %2. Created by Manish Bhobe")
         .arg(QApplication::instance()->applicationName())
         .arg(QApplication::instance()->organizationName()));

   QObject::connect(_drawWindow, SIGNAL(doodleModified2(bool)), this, SLOT(doodleModified(bool)));
   setCentralWidget(_drawWindow);
   // resize(640, 480);
   resize(QGuiApplication::primaryScreen()->availableSize() * 3 / 5);
   doodleModified(false);
}

void MainWindow::createActions()
{
   Q_ASSERT(_drawWindow != nullptr);
   fileNewAction = new QAction(QIcon(":/icons/fileNew.png"), tr("&New"), this);
   fileNewAction->setShortcut(tr("Ctrl+N"));
   fileNewAction->setStatusTip(tr("Create a new scribble document."));
   QObject::connect(fileNewAction, SIGNAL(triggered()), _drawWindow, SLOT(fileNew()));

   fileOpenAction = new QAction(QIcon(":/icons/fileOpen.png"), tr("&Open..."), this);
   fileOpenAction->setShortcut(tr("Ctrl+O"));
   fileOpenAction->setStatusTip(tr("Open scribble document from disk file."));
   QObject::connect(fileOpenAction, SIGNAL(triggered()), _drawWindow, SLOT(fileOpen()));

   fileSaveAction = new QAction(QIcon(":/icons/fileSave.png"), tr("&Save"), this);
   fileSaveAction->setShortcut(tr("Ctrl+S"));
   fileSaveAction->setStatusTip(tr("Save scribble document to disk file."));
   QObject::connect(fileSaveAction, SIGNAL(triggered()), _drawWindow, SLOT(fileSave()));

   fileSaveAsAction = new QAction(QIcon(":/icons/fileSaveAs.png"), tr("Save &as..."), this);
   fileSaveAsAction->setStatusTip(tr("Save scribble document to disk with different name."));
   QObject::connect(fileSaveAsAction, SIGNAL(triggered()), _drawWindow, SLOT(fileSaveAs()));

   exitAction = new QAction(tr("E&xit"), this);
   exitAction->setStatusTip(tr("Save all pending changes and quit application."));
   QObject::connect(exitAction, SIGNAL(triggered()), this, SLOT(exitApp()));

   penWidthAction = new QAction(QIcon(":/icons/penWidth.png"), tr("Change pen &width..."), this);
   penWidthAction->setShortcut(tr("Ctrl+W"));
   penWidthAction->setStatusTip(tr("Change the width of default pen."));
   QObject::connect(penWidthAction, SIGNAL(triggered()), _drawWindow, SLOT(changePenWidth()));

   penColorAction = new QAction(QIcon(":/icons/penColor.png"), tr("Change pen &color..."), this);
   penColorAction->setShortcut(tr("Ctrl+L"));
   penColorAction->setStatusTip(tr("Change the color of default pen."));
   QObject::connect(penColorAction, SIGNAL(triggered()), _drawWindow, SLOT(changePenColor()));

   aboutQtAction = new QAction(tr("&About Qt..."), this);
   aboutQtAction->setStatusTip(tr("Display information Qt Library used."));
   QObject::connect(aboutQtAction, SIGNAL(triggered()), qApp, SLOT(aboutQt()));

   aboutAction = new QAction(QIcon(":/icons/about.png"), tr("&About..."), this);
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
   helpMenu->addAction(aboutQtAction);
   helpMenu->addAction(aboutAction);

   menuBar()->addMenu(fileMenu);
   menuBar()->addMenu(optionsMenu);
   menuBar()->addMenu(helpMenu);
}

void MainWindow::createToolBar()
{
   QToolBar *toolBar = new QToolBar(tr("Main"), this);
   toolBar->addAction(fileNewAction);
   toolBar->addAction(fileOpenAction);
   toolBar->addAction(fileSaveAction);
   toolBar->addAction(fileSaveAsAction);
   toolBar->addSeparator();
   toolBar->addAction(penWidthAction);
   toolBar->addAction(penColorAction);
   toolBar->addSeparator();
   toolBar->addAction(aboutAction);
   addToolBar(toolBar);
}

void MainWindow::createStatusBar()
{
   // the first call to statusBar() automatically creates one!
   statusBar()->showMessage(WindowTitle);
}

void MainWindow::exitApp()
{
   close();
}

void MainWindow::about()
{
   QString str;
   QTextStream ostr(&str);
   ostr << "<html><b>Qt Scribble</b> - Doodling application<p/>Developed with the Qt " << QT_VERSION_STR
        << " C++ framework.<p/><p/>Written by - Manish Bhobe.<p/><p/>"
        << "<small>Program developed for illustration purposes only! Use at your own "
        << "risk! Author is not responsible for any damages (direct or indirect) that "
        << "may result from the use of this program.</small></html>";
   QMessageBox::about(this, AppTitle, str);
}

void MainWindow::doodleModified(bool modified)
{
   fileSaveAction->setEnabled(modified);
   QString winTitle;
   QTextStream ostr(&winTitle);
   ostr << WindowTitle << " - [" << _drawWindow->getDoodle()->filePath() << "]" << (modified ? "*" : "");
   setWindowTitle(winTitle);
}
