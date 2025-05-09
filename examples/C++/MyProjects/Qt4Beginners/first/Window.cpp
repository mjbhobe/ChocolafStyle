#include "Window.h"
#include <QApplication>
#include <QFont>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QRandomGenerator>
#include <QSlider>
#include <QVBoxLayout>

Window::Window(QWidget* parent) : QWidget{parent}
{
  m_slider = new QSlider(Qt::Orientation::Horizontal, this);
  m_slider->setRange(0, 100);
  m_slider->setGeometry(10, 10, 120, 30);

  m_label = new QLabel("Value", this);
  m_label->setGeometry(140, 10, 50, 30);

  m_btn = new QPushButton("Click to quit", this);
  m_btn->setToolTip("Qt makes C++ GUI programming easy!");
  m_btn->setGeometry(10, 50, 180, 30);
  //    QFont font("Consolas", 11);
  //    m_btn->setFont(font);
  m_btn->setIcon(QIcon::fromTheme("face-smile-big"));

  // signals & slots
  QObject::connect(m_btn, SIGNAL(clicked()), QApplication::instance(), SLOT(quit()));
  QObject::connect(m_slider, SIGNAL(valueChanged(int)), m_label, SLOT(setNum(int)));

  // initialize slider at random int between (0, 100) to fire signal
  // the label next to the slider should show random value
  int val = QRandomGenerator::global()->bounded(0, 100);
  m_slider->setValue(val);
}
