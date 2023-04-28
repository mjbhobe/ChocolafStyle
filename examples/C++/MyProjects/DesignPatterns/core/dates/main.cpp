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
   QDate today = QDate::currentDate();
   // default format
   cout << "Today is " << today.toString() << Qt::endl;
   // my favourite format
   cout << "Today is " << today.toString("dd-MMM-yy") << Qt::endl;
   // here is the default format
   cout << "Today is " << today.toString("ddd MMM dd yyyy") << Qt::endl;
   // really long format
   cout << "Today is " << today.toString("dddd MMMM dd yyyy") << Qt::endl;

   QDate bday(1969, 6, 22); // yeah, I'm really old :(
   cout << "I was born on " << bday.toString("dd-MMM-yy")
        << " which makes me approximately " << today.year() - bday.year()
        << " years old! (Maaaaaan...that's palaeolithic old :D!!)" << Qt::endl;
   // QDate today = today;
   cout << "I have been alive for " << bday.daysTo(today) << " days (beat that!)"
        << Qt::endl;
   // how many days to my next birthday?
   auto year = (today.month() > bday.month()) ? today.year() + 1 : today.year();
   QDate nextBday = QDate(year, bday.month(), bday.day());
   cout << "There are " << today.daysTo(nextBday) << " days until my next birthday ("
        << nextBday.toString("dd-MMM-yy") << ")" << Qt::endl;
   auto yearsOld{today.year() - bday.year()};
   cout << "Another " << RETIREMENT_AGE - yearsOld << " years till retirement, and "
        << PLATINUM_JUBLEE - yearsOld << " years to go to celebrate my platinum jublee!!"
        << Qt::endl;
   auto wifeys_bday = QDate(1976, 1, 22);
   year = (today.month() > wifeys_bday.month()) ? today.year() + 1 : today.year();
   auto wifeys_next_bday = QDate(year, wifeys_bday.month(), wifeys_bday.day());
   auto days_to_wifeys_next_bday = today.daysTo(wifeys_next_bday);
   cout << "My wife's birthday is coming up in "
        << (days_to_wifeys_next_bday <= 30 ? "just " : "") << days_to_wifeys_next_bday
        << " days" << (days_to_wifeys_next_bday <= 30 ? "!! " : ". ") << "It's on "
        << wifeys_next_bday.toString("dd-MMM-yy");
   if (days_to_wifeys_next_bday <= 30)
      cout << " and I have not though of a gift yet. I'm screwed!!";
   cout << Qt::endl;
   auto daughters_bday = QDate(2007, 5, 8);
   year = (today.month() > daughters_bday.month()) ? today.year() + 1 : today.year();
   auto daughters_next_bday = QDate(year, daughters_bday.month(), daughters_bday.day());
   cout << "My daughter's birthday is coming up in " << today.daysTo(daughters_next_bday)
        << " days. It's on " << daughters_next_bday.toString("dd-MMM-yy");
   if (today.daysTo(daughters_next_bday) <= 30)
      cout << " and I have not though of a gift yet. I'm screwed!!";
   cout << Qt::endl;

   return EXIT_SUCCESS;
}
