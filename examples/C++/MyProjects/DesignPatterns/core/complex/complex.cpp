// complex.cc - implementation of Complex class
#include "complex.h"
#include <QObject>
#include <QTextStream>

Complex::Complex() : QObject(), m_r(0.0), m_i(0.0) {
  // not much eelse :)
}

Complex::Complex(double r) : QObject(), m_r(r), m_i(0.0) {
  // not much eelse :)
}

Complex::Complex(double r, double i) : QObject(), m_r(r), m_i(i) {
  // not much eelse :)
}

QString Complex::toString() const {
  QString s = QString("%1 %2 %3j")
                  .arg(m_r, 6, 'f', 2)
                  .arg((m_i < 0) ? '-' : '+')
                  .arg(qAbs(m_i), 6, 'f', 2);
  return s;
}

// friend
QTextStream &operator<<(QTextStream &out, const Complex &c) {
  out << c.toString() << Qt::flush;
  return out;
}
