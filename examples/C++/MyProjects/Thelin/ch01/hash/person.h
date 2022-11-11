// person.h - declares Person class
#ifndef __Person_h__
#define __Person_h__

#include <QHash>
#include <QObject>
#include <QTextStream>

class Person : public QObject {
  public:
    Person(const QString& name, const QString& number, QObject* parent = nullptr);
    Person(const Person& p);

    const QString& name() const;
    const QString& number() const;
    friend QTextStream& operator<<(QTextStream&, const Person&);

  private:
    QString m_name;
    QString m_number;
};

bool operator == (const Person& p1, const Person& p2);
uint qHash(const Person& key);

#endif  // __Person_h__
