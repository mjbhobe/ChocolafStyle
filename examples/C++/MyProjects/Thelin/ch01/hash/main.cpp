// main.cpp
#include "person.h"
#include <QHash>
#include <QObject>
#include <QSet>
#include <QTextStream>

QTextStream cout(stdout, QIODeviceBase::WriteOnly);

template<class T>
QTextStream& operator<<(QTextStream& os, QList<T> lst)
{
  foreach (T value, lst)
    os << value << " ";
  return os;
}

int main(int, char**)
{
  QHash<Person, int> hashmap;

  hashmap[ Person("Anders", "8447070") ] = 10;
  hashmap[ Person("Micke", "7728433") ] = 20;

  cout << "Hash value " << hashmap.value(Person( "Anders", "8447070" )) << Qt::endl;
  cout << "Hash value " << hashmap.value(Person("Anders", "8447071")) << Qt::endl;
  cout << "Hash value " << hashmap.value(Person("Micke", "7728433")) << Qt::endl;
  cout << "Hash value " << hashmap.value(Person("Michael", "7728433")) << Qt::endl;

  cout << "QSet example..." << Qt::endl;
  QSet<QString> set;
  set << "Ada"
      << "C++"
      << "Python"
      << "C++" // should be dropped
      << "Oracle"
      << "Ada"; // this too!
  // should print Ada & C++ only once!
  for (QSet<QString>::ConstIterator iter = set.begin(); iter != set.end(); ++iter)
    cout << *iter << " ";
  cout << Qt::endl;
  cout << "set.contains(\"Fortran\")? " << (set.contains("Fortran") ? "Yes" : "No") << Qt::endl;
  // multi-map
  QMultiMap<QString, int> multiMap;
  multiMap.insert("foo", 10);
  multiMap.insert("bar", 20);
  multiMap.insert("foo", 30);
  cout << "QMultiMap<QString, int> test -> multiMap[\"foo\"] = " << multiMap.values("foo")
       << Qt::endl;

  return 0;
}



