#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QPainter>
#include <QString>
#include <fmt/core.h>
#include <format>

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent), ui(new Ui::MainWindow)
{
   ui->setupUi(this);
}

MainWindow::~MainWindow() { delete ui; }

void MainWindow::paintEvent(QPaintEvent * /*event*/)
{
   QPainter painter(this);
   painter.setRenderHint(QPainter::Antialiasing);
   std::string hello = std::format("Welcome to Qt{} programming with C++", QT_VERSION_STR);
   QString msg(hello.c_str());
   painter.setPen(this->palette().color(QPalette::WindowText));
   painter.drawText(10, 10, msg);
}
