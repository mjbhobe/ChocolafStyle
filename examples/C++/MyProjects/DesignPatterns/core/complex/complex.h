#ifndef __Complex_h__
#define __Complex_h__

#include <QObject>
#include <QTextStream>

class Complex : public QObject {
public:
  Complex();
  Complex(double r);
  Complex(double r, double i);
  QString toString() const;

  friend QTextStream &operator<<(QTextStream &out, const Complex &c);

protected:
  double m_r, m_i;
};

#endif // __Complex_h__
