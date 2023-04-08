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
   cout << "I was born on " << bday.toString("dd-MMM-yy")
        << " which makes me approximately " << QDate::currentDate().year() - bday.year()
        << " years old! (maaaaaan!! that's fossil old :D)" << Qt::endl;
   QDate today = QDate::currentDate();
   cout << "I have been alive for " << bday.daysTo(today) << " days! (beat that)"
        << Qt::endl;
   // how many days to my next birthday?
   auto year = (today.month() > bday.month()) ? today.year() + 1 : today.year();
   QDate nextBday = QDate(year, bday.month(), bday.day());
   cout << "There are " << today.daysTo(nextBday) << " days until my next birthday ("
        << nextBday.toString("dd-MMM-yy") << ")" << Qt::endl;
   auto yearsOld{QDate::currentDate().year() - bday.year()};
   cout << "Another " << RETIREMENT_AGE - yearsOld << " years till retirement, and "
        << PLATINUM_JUBLEE - yearsOld << " years to go to celebrate my platinum jublee!!"
        << Qt::endl;
   auto anus_bday = QDate(1976, 1, 22);
   year = (today.month() > anus_bday.month()) ? today.year() + 1 : today.year();
   auto anus_next_bday = QDate(year, anus_bday.month(), anus_bday.day());
   auto days_to_anus_next_bday = today.daysTo(anus_next_bday);
   cout << "My wife's birthday is coming up in "
        << (days_to_anus_next_bday <= 30 ? "just " : "") << days_to_anus_next_bday
        << " days" << (days_to_anus_next_bday <= 30 ? "!! " : ". ") << "It's on "
        << anus_next_bday.toString("dd-MMM-yy");
   if (days_to_anus_next_bday <= 30)
      cout << " and I have not though of a gift yet. I'm screwed!!";
   cout << Qt::endl;
   auto nupoors_bday = QDate(2007, 5, 8);
   year = (today.month() > nupoors_bday.month()) ? today.year() + 1 : today.year();
   auto nupoors_next_bday = QDate(year, nupoors_bday.month(), nupoors_bday.day());
   cout << "Nupoor's birthday: " << nupoors_next_bday.toString("dd-MMM-yy")
        << " coming up in " << today.daysTo(nupoors_next_bday) << " days!" << Qt::endl;

   return EXIT_SUCCESS;
}
