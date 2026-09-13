#ifndef __ConversionObserver_h__
#define __ConversionObserver_h__

#include <QObject>

class ConversionObserver : public QObject {
    Q_OBJECT
  public:
    explicit ConversionObserver(QObject *parent = nullptr);

  public slots:
    void handleTemperatureConverted(double celsius, double fahrenheit);
    void handleDistanceConverted(double meters, double feet);
    void handleWeightConverted(double grams, double pounds);
    void handleVolumeConverted(double liters, double fluidOunces);
};

#endif // __ConversionObserver_h__
