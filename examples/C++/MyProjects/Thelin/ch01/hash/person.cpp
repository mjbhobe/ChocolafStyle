// person.cpp = implements Person class
#include <QObject>
#include <QHash>
#include "person.h"

Person::Person(const QString& name, const QString& number, QObject* parent /*=nullptr*/)
  : QObject(parent)
{
  m_name = name;
  m_number = number;
}

Person::Person(const Person& other)
{
  if (this != &other) {
    m_name = other.m_name;
    m_number = other.m_number;
  }
}

const QString& Person::name() const
{
  return m_name;
}

const QString& Person::number() const
{
  return m_number;
}

bool operator == (const Person& p1, const Person& p2)
{
  return (p1.name() == p2.name()) && (p1.number() == p2.number());
}

uint qHash(const Person& key)
{
  return qHash(key.name()) ^ qHash(key.number());
}

QTextStream& operator<<(QTextStream& ts, const Person& p)
{
  ts << p.name() << "[" << p.number() << "]";
  return ts;
}
