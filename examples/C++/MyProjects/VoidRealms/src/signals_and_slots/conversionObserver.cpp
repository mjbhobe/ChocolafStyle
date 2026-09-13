#include "conversionObserver.h"
#include <QObject>
#include <print>

ConversionObserver::ConversionObserver(QObject *parent) : QObject(parent) {}

void ConversionObserver::handleTemperatureConverted(
    double celsius, double fahrenheit)
{
  std::println("{:.3f} Celsius is {:.3f} Fahrenheit", celsius, fahrenheit);
}

void ConversionObserver::handleDistanceConverted(double meters, double feet)
{
  std::println("{:.3f} Meters is {:.3f} Feet", meters, feet);
}

void ConversionObserver::handleWeightConverted(double grams, double pounds)
{
  std::println("{:.3f} Grams is {:.3f} Pounds", grams, pounds);
}

void ConversionObserver::handleVolumeConverted(
    double liters, double fluidOunces)
{
  std::println("{:.3f} Liters is {:.3f} Fluid Ounces", liters, fluidOunces);
}
