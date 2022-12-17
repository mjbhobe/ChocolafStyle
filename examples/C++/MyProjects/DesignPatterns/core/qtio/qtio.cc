// qtio.cc - i/o with Qt Text Streams
#include <QtCore>
#include <cstdio>
#include <cstdlib>

static QTextStream cout(stdout, QIODevice::WriteOnly);
static QTextStream cerr(stderr, QIODevice::WriteOnly);
static QTextStream cin(stdin, QIODevice::ReadOnly);

int main(int argc, char **argv)
{
   QCoreApplication app(argc, argv);
   QDate today = QDate::currentDate();
   int thisYear = today.year();

   fflush(stdin);
   QString name;
   cout << "Your name? " << Qt::flush;
   name = cin.readLine();
   int birthYear;
   cout << "Your birth year? " << Qt::flush;
   cin >> birthYear;
   cout << "Hello " << name << " next year you'll be approx. " << (thisYear - birthYear + 1)
        << " years old" << Qt::endl;

   return EXIT_SUCCESS;
}
