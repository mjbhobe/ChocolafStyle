#include <cstdio>
#include <cstdlib>
#include <QCoreApplication>
#include <QDate>
#include <QTextStream>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);

   // display today's date
   // default format
   cout << "Today is " << QDate::currentDate().toString() << Qt::endl;
   // my favourite format
   cout << "Today is " << QDate::currentDate().toString("dd-MMM-yy") << Qt::endl;
   // here is the default format
   cout << "Today is " << QDate::currentDate().toString("ddd MMM dd yyyy") << Qt::endl;
   // really long format
   cout << "Today is " << QDate::currentDate().toString("dddd MMMM dd yyyy") << Qt::endl;

   QDate bday(1969, 6, 22); // yeah, I'm really old :(
   cout << "I was born on " << bday.toString("dd-MMM-yy")
        << " which makes me approximately " << QDate::currentDate().year() - bday.year()
        << " years old!" << Qt::endl
        << "\t\t (man that's fossil old!!)" << Qt::endl;
   QDate today = QDate::currentDate();
   cout << "I have been alive for " << bday.daysTo(today) << " days! (beat that)"
        << Qt::endl;
   // how many days to my next birthday?
   auto year = (today.month() > bday.month()) ? today.year() + 1 : today.year();
   QDate nextBday = QDate(year, bday.month(), bday.day());
   cout << "There are " << today.daysTo(nextBday) << " days until my next birthday ("
        << nextBday.toString("dd-MMM-yy") << ")" << Qt::endl;
   auto yearsOld{QDate::currentDate().year() - bday.year()};
   cout << "Another " << 60 - yearsOld << " years till retirement, and " << 75 - yearsOld
        << " years to go to celebrate my platinum jublee!!" << Qt::endl;

   return EXIT_SUCCESS;
}
