#include <QCoreApplication>
#include <QTimer>

#include "conversionObserver.h"
#include "unitConverter.h"

int main(int argc, char *argv[])
{
  QCoreApplication app(argc, argv);

  UnitConverter converter;
  ConversionObserver observer;

  // Compile-time checked pointer-to-member signal/slot wiring
  QObject::connect(&converter, &UnitConverter::temperatureConverted, &observer,
      &ConversionObserver::handleTemperatureConverted);

  QObject::connect(&converter, &UnitConverter::distanceConverted, &observer,
      &ConversionObserver::handleDistanceConverted);

  QObject::connect(&converter, &UnitConverter::weightConverted, &observer,
      &ConversionObserver::handleWeightConverted);


  QObject::connect(&converter, &UnitConverter::volumeConverted, &observer,
      &ConversionObserver::handleVolumeConverted);

  // Queue executions on the running event loop
  QTimer::singleShot(0, [&converter]() {
    converter.setCelsius(100.0);
    converter.setMeters(42.195);
    converter.setGrams(500.0);
    converter.setLiters(3.65);

    QCoreApplication::quit();
  });

  return app.exec();
}
