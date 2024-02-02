// tempConv/main.cc - temperature converter (signal & slots handling)
#include "widget.h"
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QSlider>
#include <QSpinBox>
#include <QTextStream>
#include <QVBoxLayout>

float c2f(int celcius)
{
  float farenheit = static_cast<float>((celcius * (9.0 / 5.0)) + 32.0);
  return farenheit;
}

void setupGui(QWidget &window)
{
  const int min_celcius = -100, max_celcius = 100;

  window.setWindowTitle("Qt Signals & Slots");
  QSpinBox *spinner = new QSpinBox();
  QSlider *slider = new QSlider(Qt::Horizontal);
  QLabel *faren = new QLabel("");
  QLabel *qtVer = new QLabel("");
  QPushButton *quit = new QPushButton("Quit!");
  spinner->setRange(min_celcius, max_celcius);
  slider->setRange(min_celcius, max_celcius);
  QString qtVersion;
  QTextStream ostr(&qtVersion);
  ostr << "You are using Qt " << QT_VERSION_STR;
  qtVer->setText(qtVersion);

  //slider->setRange(c2f(min_celcius), c2f(max_celcius));
  // as a first step, we will just connect spinner to slider, so that
  // spinning one will move the other
  QObject::connect(spinner, SIGNAL(valueChanged(int)), slider, SLOT(setValue(int)));
  QObject::connect(spinner, SIGNAL(valueChanged(int)), faren, SLOT(setNum(int)));
  QObject::connect(slider, SIGNAL(valueChanged(int)), spinner, SLOT(setValue(int)));
  QObject::connect(quit, SIGNAL(clicked()), qApp, SLOT(quit()));

  // arrange the widgets
  QHBoxLayout *widgets = new QHBoxLayout();
  widgets->addWidget(spinner);
  widgets->addWidget(slider);
  widgets->addWidget(faren);
  QHBoxLayout *buttons = new QHBoxLayout();
  buttons->addWidget(qtVer);
  buttons->addStretch();
  buttons->addWidget(quit);

  QVBoxLayout *l = new QVBoxLayout;
  l->addLayout(widgets);
  l->addLayout(buttons);
  window.setLayout(l);
  spinner->setValue(20);
}

int main(int argc, char **argv)
{
  QApplication app(argc, argv);
  QApplication::setFont(QApplication::font("QMenu"));
  app.setStyle("Fusion");

  // create & show GUI
  Widget window;
  window.show();

  return app.exec();
}
