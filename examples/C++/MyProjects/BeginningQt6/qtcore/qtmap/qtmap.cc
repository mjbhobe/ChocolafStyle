// qtmap.cc - using QMap class
#include <QtCore>

// DON'T USE <iostream> - all other std includes & data structures are Ok!
static QTextStream cout(stdout, QIODevice::WriteOnly);
// NOTE: this may not work on Windows!
QLocale locale(QLocale::English, QLocale::India);

/**
 * @brief abstraction of an Employee with name, age and salary
 */
class Employee
{
protected:
   QString _name;
   int _age;
   double _salary;

public:
   Employee() : _name{""}, _age{0}, _salary{0.0}
   {
      // nothing more
   }

   Employee(const QString &name, int age, double salary)
       : _name(name), _age(age), _salary(salary)
   {
      // nothing more
   }

   // copy ctor
   Employee(const Employee &other)
   {
      this->_name = other._name;
      this->_age = other._age;
      this->_salary = other._salary;
   }

   // assignment operator
   Employee &operator=(const Employee &other)
   {
      if (this != &other) {
         this->_name = other._name;
         this->_age = other._age;
         this->_salary = other._salary;
      }
      return *this;
   }

   friend QTextStream &operator<<(QTextStream &out, const Employee &emp)
   {
      out << "Name: " << emp._name << " - age: " << emp._age
          << " - salary: " << qPrintable(locale.toCurrencyString(emp._salary))
          << Qt::endl;
      return out;
   }
};

int main(int argc, char **argv)
{
   QCoreApplication app(argc, argv);

   // some info about locale
   cout << "Currency symbol: " << locale.currencySymbol() << Qt::endl;

   QMap<QString, int> actorMovieCount{
       {"Sean Connery", 25},
       {"Jude Law", 40},
       {"Amitabh Bacchan", 175},
       {"Dipika Padukone", 45},
       {"Priyanka Chopra", 55},
   };

   for (auto actor : actorMovieCount.keys())
      cout << actor << " has acted in " << actorMovieCount[actor] << " movies"
           << Qt::endl;

   QMap<int, Employee> empList = {
       {100, {"Manish", 52, 75432.45}},
       {175, {"Anupa", 45, 9587687.67}},
       {300, {"Nupoor", 15, 15432.00}},
       {550, {"Sunila", 81, 345678.34}},
   };

   for (auto empNo : empList.keys())
      cout << empNo << " -> " << empList[empNo];

   // return app.exec();
   return 0;
}
