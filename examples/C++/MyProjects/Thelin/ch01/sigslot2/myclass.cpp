// myclass.cpp - implementation of MyClass
#include "myclass.h"
#include <QTextStream>

MyClass::MyClass(const QString &str, QObject *parent /*=nullptr*/) : QObject(parent)
{
  m_string = str;
}

const QString &MyClass::text() const
{
  return m_string;
}

size_t MyClass::getLengthOfString() const
{
  return m_string.length();
}

void MyClass::setText(const QString &str)
{
  if (m_string != str) {
    m_string = str;
    emit textChanged(m_string);
  }
}

// friend
QTextStream &operator<<(QTextStream &ost, const MyClass &cls)
{
  ost << cls.text();
  return ost;
}
