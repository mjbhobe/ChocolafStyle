// C2F.cpp : implements the Celcius to Farenheit converter

#include <QObject>
#include "C2F.h"


C2F::C2F(QObject *parent /*=nullptr*/)
    : QObject(parent),
      _celcius{0.0f}
{
  // nothing more
}

void C2F::setCelcius(float celcius)
{
  if (_celcius != celcius) {
    _celcius = celcius;
    // calculate farenheit
    float far = (_celcius * 1.8) + 32.0f;
    emit c2f(celcius, far);
  }
}
