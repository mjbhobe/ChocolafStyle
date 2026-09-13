#include <QDebug>
#include <QObject>

#include "unitConverter.h"

UnitConverter::UnitConverter(QObject *parent) : QObject(parent) {}

void UnitConverter::setCelsius(double celsius)
{
  const double fahrenheit = (celsius * 9.0 / 5.0) + 32.0;
  emit temperatureConverted(celsius, fahrenheit);
}

void UnitConverter::setMeters(double meters)
{
  constexpr double metersToFeetRatio = 3.28084;
  const double feet                  = meters * metersToFeetRatio;
  emit distanceConverted(meters, feet);
}

void UnitConverter::setGrams(double grams)
{
  constexpr double gramsToPoundsRatio = 0.00220462;
  const double pounds                 = grams * gramsToPoundsRatio;
  emit weightConverted(grams, pounds);
}

void UnitConverter::setLiters(double liters)
{
  constexpr double litersToFluidOuncesRatio = 33.814;
  const double fluidOunces                  = liters * litersToFluidOuncesRatio;
  emit volumeConverted(liters, fluidOunces);
}
