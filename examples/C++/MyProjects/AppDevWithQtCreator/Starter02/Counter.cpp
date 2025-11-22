// Counter.cpp - implementation of Counter class
//
#include <QObject>
#include "Counter.h"

void Counter::setValue(int newValue) {
  if (newValue != m_value) {
    m_value = newValue;
    // emit signal since value has changed
    emit valueChanged(m_value);
  }
}

void Counter::increment() { setValue(m_value + 1); }

void Counter::decrement() { setValue(m_value - 1); }
