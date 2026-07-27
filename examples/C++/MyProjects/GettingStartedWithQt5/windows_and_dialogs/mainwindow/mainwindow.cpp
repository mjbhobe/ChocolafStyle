#include <QAction>
#include <QApplication>
#include <QLabel>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QPixmap>
#include <QString>
#include <QToolBar>
#include <print>
#include "mainwindow.h"

#ifndef IMAGES_PATH
#error "FATAL: IMAGES_PATH not defined on compiler command line!"
#endif

MainWindow::MainWindow()
    : QMainWindow(), m_fileMenu{nullptr}, m_helpMenu{nullptr}
{
  m_label = new QLabel("Central Widget of MainWindow");
  m_label->setAlignment(Qt::AlignmentFlag::AlignCenter);
  setCentralWidget(m_label);

  createActions();
  // setup toolbar
  m_toolBar = addToolBar("Main Toolbar");
  m_toolBar->addAction(m_newAction);
  m_toolBar->addAction(m_openAction);
  m_toolBar->addSeparator();
  m_toolBar->addAction(m_quitAction);
}

void MainWindow::createActions()
{
  std::println("IMAGES_PATH = {}", IMAGES_PATH);
  QPixmap newIcon(QString(IMAGES_PATH) + "/file_new.png");
  QPixmap openIcon(QString(IMAGES_PATH) + "/file_open.png");
  QPixmap exitIcon(QString(IMAGES_PATH) + "/exit.png");

  // file menu
  m_newAction = new QAction(newIcon, "&New", this);
  m_newAction->setShortcuts(QKeySequence::New);
  m_openAction = new QAction(openIcon, "&Open", this);
  m_openAction->setShortcuts(QKeySequence::Open);
  m_quitAction = new QAction(exitIcon, "&Quit", this);
  m_quitAction->setShortcuts(QKeySequence::Quit);
  m_fileMenu = menuBar()->addMenu("&File");
  m_fileMenu->addAction(m_newAction);
  m_fileMenu->addAction(m_openAction);
  m_fileMenu->addSeparator();
  m_fileMenu->addAction(m_quitAction);
  // help menu
  m_aboutAction = new QAction("About...", this);
  m_aboutAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_H)); // Ctrl+H
  m_helpMenu = menuBar()->addMenu("&Help");
  m_helpMenu->addAction(m_aboutAction);

  // setup signals & slots
  QObject::connect(
      m_newAction, &QAction::triggered, this, &MainWindow::fileNew);
  QObject::connect(
      m_openAction, &QAction::triggered, this, &MainWindow::fileOpen);
  QObject::connect(
      m_quitAction, &QAction::triggered, this, &QApplication::quit);
  QObject::connect(
      m_aboutAction, &QAction::triggered, this, &MainWindow::about);
}

void MainWindow::about()
{
  // Title of the dialog
  QString title = windowTitle();

  // Rich text / HTML content for the body
  constexpr std::string_view rawHtmlTemplate = R"(
      <h3>My Qt Application v1.0.0</h3>
      <p>Developed with C++20 and Qt{}.</p>
      <p>Copyright &copy; 2026 Manish Bhobe. All rights reserved.</p>
      <p>Visit our website: <a href='https://namostute.com'>namostute.com</a></p>
  )";
  std::string text = std::format(rawHtmlTemplate, QT_VERSION_STR);

  // Display the about box
  QMessageBox::about(this, title, QString::fromStdString(text));
}

void MainWindow::fileNew()
{
  QMessageBox::information(this, windowTitle(),
      QString("You clicked File->New\nYet to be implemented!"));
}

void MainWindow::fileOpen()
{
  QMessageBox::information(this, windowTitle(),
      QString("You clicked File->Open\nYet to be implemented!"));
}
