// mainWindow.cpp - implementation of MainWindow class
//
#include <QApplication>
#include <QDebug>
#include <format>
#include "mainWindow.h"
#include "ui_mainWindow.h"

MainWindow::MainWindow(QWidget *parent)
  : QMainWindow(parent), ui(new Ui::MainWindow), counter(nullptr) {
  // initialize counter
  counter = new Counter(this);
  // load UI from file
  ui->setupUi(this);
  // save pointers to widgets on form
  helloLabel      = ui->helloLabel;
  counterLabel    = ui->counterLabel;
  closeBtn        = ui->closeBtn;
  counterPlusBtn  = ui->counterPlusBtn;
  counterMinusBtn = ui->counterMinusBtn;

  helloLabel->setText(QString::fromStdString(std::format("Welcome to Qt {}", QT_VERSION_STR)));
  //counterLabel->setText(QString::number(1024));

  // setup signals & slots
  //QObject::connect(closeBtn, SIGNAL(clicked()), this, SLOT(onClose()));
  QObject::connect(closeBtn, &QPushButton::clicked, this, &MainWindow::onClose);
  // counterPlusBtn clicked -> increment counter -> set value for label
  // QObject::connect(counterPlusBtn, SIGNAL(clicked()), counter, SLOT(increment()));
  QObject::connect(counterPlusBtn, &QPushButton::clicked, counter, &Counter::increment);
  // counterMinusBtn clicked -> decrement counter -> set value for label
  // QObject::connect(counterMinusBtn, SIGNAL(clicked()), counter, SLOT(decrement()));
  QObject::connect(counterMinusBtn, &QPushButton::clicked, counter, &Counter::decrement);
  // and here is the lamda to handle the valueChanged() signal emitted by the Counter instance
  QObject::connect(counter, &Counter::valueChanged,
    // we use a lamda to handle the slot
    [this](int value) {
      counterLabel->setText(QString::number(value));
    }
  );
}

MainWindow::~MainWindow() {
  // free up loaded UI definitions
  delete ui;
}

// slot
void MainWindow::onClose() {
  qDebug() << "In MainWindow::onClose()";
  QApplication::exit();
}

void MainWindow::onCounterBtnClicked() {
  // implementation
}
