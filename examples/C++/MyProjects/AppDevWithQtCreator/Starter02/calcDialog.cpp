// calcDialog.cpp - implementation of CalcDialog class
//
#include <QDialog>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QDebug>

#include "calcDialog.h"
#include "ui_calcDialog.h"

CalcDialog::CalcDialog(QWidget *parent)
  : QDialog(parent), ui(new Ui::CalcDialog)
{
  // load UI from definition
  ui->setupUi(this);
  // save pointers to objects on UI
  plusBtn     = ui->plusBtn;
  minusBtn    = ui->minusBtn;
  multiplyBtn = ui->multiplyBtn;
  divideBtn   = ui->divideBtn;
  closeBtn    = ui->closeBtn;
  op1Txt      = ui->op1Txt;
  op2Txt      = ui->op2Txt;
  resultLbl   = ui->resultLbl;

  // setup signals & slots
  QObject::connect(closeBtn, &QPushButton::clicked, this, &QDialog::accept);
  QObject::connect(plusBtn, &QPushButton::clicked, [this]() { this->performOp('+'); });
  QObject::connect(minusBtn, &QPushButton::clicked, [this]() { this->performOp('-'); });
  QObject::connect(multiplyBtn, &QPushButton::clicked, [this]() { this->performOp('*'); });
  QObject::connect(divideBtn, &QPushButton::clicked, [this]() { this->performOp('/'); });
  QObject::connect(op1Txt, SIGNAL(textChanged(const QString&)), this, SLOT(enableOpsBtns()));
  QObject::connect(op2Txt, SIGNAL(textChanged(const QString&)), this, SLOT(enableOpsBtns()));
  resultLbl->setText("");
}

CalcDialog::~CalcDialog()
{
  // cleanup loaded UI definitions
  delete ui;
}

void CalcDialog::enableOpsBtns()
{
  // enables all operator buttons when op1Txt & op2Txt
  // controls have *numeric* text
  bool ok1, ok2, enable{false};
  QString(op1Txt->text()).toFloat(&ok1);
  QString(op2Txt->text()).toFloat(&ok2);
  if (ok1 && ok2) {
    enable = true;
  }
  plusBtn->setEnabled(enable);
  minusBtn->setEnabled(enable);
  multiplyBtn->setEnabled(enable);
  divideBtn->setEnabled(enable);
}

void CalcDialog::performOp(char op)
{
  // NOTE: all operator buttons have been enabled ONLY
  // when both operator text fields have numbers (floats) entered
  bool ok1, ok2;
  float op1 = QString(op1Txt->text()).toFloat(&ok1);
  float op2 = QString(op2Txt->text()).toFloat(&ok2);
  if (ok1 && ok2) {
    switch (op) {
      case '+':
        resultLbl->setText(QString::number(op1 + op2));
        break;
      case '-':
        resultLbl->setText(QString::number(op1 - op2));
        break;
      case '*':
        resultLbl->setText(QString::number(op1 * op2));
        break;
      case '/':
        if (op2 != 0)
          resultLbl->setText(QString::number(op1 / op2));
        else
          resultLbl->setText("Undefined! (divide by 0)");
        break;
      default:
        qDebug() << "Operation " << op << " not supported!";
    }
  }
}

