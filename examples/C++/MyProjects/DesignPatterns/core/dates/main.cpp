#include <QCoreApplication>
#include <QDate>
#include <QTextStream>
#include <cstdio>
#include <cstdlib>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);
   const int RETIREMENT_AGE{60};
   const int PLATINUM_JUBLEE{75};

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
   cout << "I was born on " << bday.toString("dd-MMM-yy") << " which makes me approximately "
        << QDate::currentDate().year() - bday.year() << " years old!"
        << "(maaaaaan!! that's fossil old :D)" << Qt::endl;
   QDate today = QDate::currentDate();
   cout << "I have been alive for " << bday.daysTo(today) << " days! (beat that)" << Qt::endl;
   // how many days to my next birthday?
   auto year = (today.month() > bday.month()) ? today.year() + 1 : today.year();
   QDate nextBday = QDate(year, bday.month(), bday.day());
   cout << "There are " << today.daysTo(nextBday) << " days until my next birthday ("
        << nextBday.toString("dd-MMM-yy") << ")" << Qt::endl;
   auto yearsOld{QDate::currentDate().year() - bday.year()};
   cout << "Another " << RETIREMENT_AGE - yearsOld << " years till retirement, and "
        << PLATINUM_JUBLEE - yearsOld << " years to go to celebrate my platinum jublee!!"
        << Qt::endl;
   auto anus_bday = QDate(2023, 1, 22);
   cout << "My wife's birthday is coming up in just " << today.daysTo(anus_bday)
        << " days!! It's on " << anus_bday.toString("dd-MMM-yy")
        << " and I have not though of a gift yet. I'm screwed!!" << Qt::endl;
   cout << "Anu's birthday: " << today.addDays(36).toString("dd-MMM-yy") << " coming up in "
        << today.daysTo(anus_bday) << " days!" << Qt::endl;
   auto nupoors_bday = QDate(today.year() + 1, 5, 8);
   cout << "Nupoor's birthday: " << nupoors_bday.toString("dd-MMM-yy") << " coming up in "
        << today.daysTo(nupoors_bday) << " days!" << Qt::endl;

   return EXIT_SUCCESS;
}