// widget.cpp: implementation of Widget class
#include "widget.h"
#include <QApplication>
#include <QDebug>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSlider>
#include <QSpinBox>
#include <QString>
#include <QTextStream>
#include <QVBoxLayout>
#include <QWidget>

const int MIN_C = -100;
const int MAX_C = 100;

Widget::Widget(QWidget *parent) : QWidget(parent)
{
   setupUi();
   setWindowTitle("Qt Temp Converter");
}

float Widget::c2f(int celcius)
{
   float faren = static_cast<float>(celcius * (9.0 / 5.0) + 32.0);
   return faren;
}

void Widget::setupUi()
{
   spinBox = new QSpinBox(this);
   slider = new QSlider(Qt::Horizontal, this);
   close = new QPushButton("Close", this);
   faren = new QLabel("");
   qtVer = new QLabel("");

   // setup controls
   spinBox->setToolTip("<html>Spin to calculate &deg;F</html>");
   close->setToolTip("Close Application");
   spinBox->setRange(MIN_C, MAX_C);
   slider->setRange(static_cast<int>(c2f(MIN_C)), static_cast<int>(c2f(MAX_C)));
   slider->setEnabled(false); // so user cannot drag it
   QRect geom = slider->geometry();
   qDebug() << "slider->geometry() " << geom;
   slider->setMinimumWidth(geom.width() + 100);
   QString str;
   QTextStream ostr(&str);
   ostr << "Build with Qt " << QT_VERSION_STR;
   qtVer->setText(str);

   // layout controls
   QHBoxLayout *layout1 = new QHBoxLayout();
   layout1->addWidget(spinBox);
   layout1->addWidget(slider);
   layout1->addWidget(faren);

   QHBoxLayout *layout2 = new QHBoxLayout();
   layout2->addWidget(qtVer);
   layout2->addStretch();
   layout2->addWidget(close);

   QVBoxLayout *mainLayout = new QVBoxLayout();
   mainLayout->addLayout(layout1);
   mainLayout->addLayout(layout2);
   setLayout(mainLayout);
   setMinimumWidth(480);

   // setup signals & slots
   QObject::connect(spinBox, SIGNAL(valueChanged(int)), this, SLOT(celciusChanged(int)));
   QObject::connect(close, SIGNAL(clicked()), qApp, SLOT(quit()));

   // and kick off
   spinBox->setValue(20);
}

void Widget::celciusChanged(int celcius)
{
   float farent = c2f(celcius);
   slider->setValue(static_cast<int>(farent));
   QString str =
         QString("<html><b>%1 &deg;F</b></html>").arg(farent, 0, 'f', 2); // %.2f format
   // str.asprintf("<html><b>%.2f &deg;F</b></html>", farent);
   faren->setText(str);
}
