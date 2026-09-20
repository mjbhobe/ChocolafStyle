#ifndef __UnitConverter_h__
#define __UnitConverter_h__

#include <QObject>

class UnitConverter : public QObject {
    Q_OBJECT
  public:
    explicit UnitConverter(QObject *parent = nullptr);

    // setters, will raise respective signals below
    void setCelsius(double celsius);
    void setMeters(double meters);
    void setGrams(double grams);
    void setLiters(double liters);

  signals:
    void temperatureConverted(double celsius, double fahrenheit);
    void distanceConverted(double meters, double feet);
    void weightConverted(double grams, double pounds);
    void volumeConverted(double liters, double fluidOunces);
};

#endif // __UnitConverter_h__
