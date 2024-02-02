#include "widget.h"
#include <QApplication>
#include <QByteArray>
#include <QDebug>
#include <QFont>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QRegExp>
#include <QRegExpValidator>
#include <QString>
#include <QTextEdit>
#include <QTextStream>
#include <QVBoxLayout>
#include <cassert>
#include <climits>
#include <gmp.h>

Widget::Widget(QWidget *parent) : QWidget(parent)
{
   label = new QLabel("Number:");
   number = new QLineEdit();
   calculate = new QPushButton("Calculate");
   quit = new QPushButton("Quit!");
   factorial = new QTextEdit("");
   setupUi();
}

void Widget::setupUi()
{
   this->setWindowTitle("Qt Factorials");

   QHBoxLayout *layout1 = new QHBoxLayout();
   layout1->addWidget(label);
   layout1->addWidget(number);
   layout1->addWidget(calculate);
   layout1->addWidget(quit);

   QVBoxLayout *main = new QVBoxLayout();
   main->addLayout(layout1);
   main->addWidget(factorial);
   this->setLayout(main);

   calculate->setToolTip("Calculate factorial");
   calculate->setEnabled(false); // disabled initially
   calculate->setDefault(true);
   quit->setToolTip("Quit application");
   factorial->setReadOnly(true);

   QFont font = QFont(QApplication::font("QMenu").family(), 9);
   factorial->setFont(font);

   QString str, str2;
   QTextStream ostr(&str);
   ostr << ULLONG_MAX;
   // max number of digits in ULLONG_MAX
   auto max_len = str.length();
   QTextStream ostr2(&str2);
   ostr2 << "[1-9][0-9]{0," << max_len - 1 << "}";
   qDebug() << "ULLONG_MAX length " << max_len << " QRegExp: " << str2;
   QRegExp regExp(str2);
   number->setValidator(new QRegExpValidator(regExp, this));

   // setup signals & slots - we'll use lamda functions here
   connect(number, &QLineEdit::textChanged,
           [=](const QString &text) { calculate->setEnabled(!text.isEmpty()); });
   connect(quit, &QPushButton::clicked, qApp, &QApplication::quit);
   connect(calculate, &QPushButton::clicked, this, &Widget::calculateFactorial);

   setMinimumSize(640, 500);
}

Widget::~Widget() {}

void Widget::calculateFactorial()
{
   // QString text = number->text();
   // QByteArray ba= text.toLocal8Bit();

   // clear any existing factorial value displayed
   factorial->clear();

   QApplication::setOverrideCursor(Qt::WaitCursor);
   mpz_t mpz_fact;
   mpz_init_set_ui(mpz_fact, 0);
   // set value from numbet->text() as const char*
   // auto flag = mpz_set_str(mpz_input, number->text().toLocal8Bit().data(), 10);
   // assert(flag == 0); // conversion successful
   // find factorial
   bool ok;
   unsigned long num = number->text().toLong(&ok, 10);

   if (ok) {
      mpz_fac_ui(mpz_fact, num);
      char *buff = new char[mpz_sizeinbase(mpz_fact, 10) + 2];
      mpz_get_str(buff, 10, mpz_fact);
      qDebug() << buff;
      factorial->setText(buff);
      delete[] buff;
   } else {
      factorial->setText("Can't convert input");
   }
   QApplication::restoreOverrideCursor();
}
