// c2f.cc - convert celcius temp to farenheit
#include "common_funcs.h"
#include <QtCore>
#include <cstdio>
#include <cstdlib>

static QTextStream cout(stdout, QIODevice::WriteOnly);
static QTextStream cerr(stderr, QIODevice::WriteOnly);
static QTextStream cin(stdin, QIODevice::ReadOnly);

int main(int argc, char **argv)
{
   QCoreApplication app(argc, argv);
   float celcius{0.0f};
   float farenheit{0.0f};
   QString strCelcius{""};
   bool ok{false};
   fflush(stdin);

   do {
      cout << "Celcius temp (enter to quit)? " << Qt::flush;
      strCelcius = cin.readLine();
      if (strCelcius.trimmed().length() != 0) {
         celcius = strCelcius.toFloat(&ok);
         if (!ok) {
            cerr << "FATAL " << strCelcius << " - not numeric!" << Qt::endl;
         }
         else {
            farenheit = (celcius * (9.0f / 5.0f)) + 32.0f;
            QString msg = QString("%1 C = %2 F").arg(celcius, 6, 'f', 2).arg(farenheit, 6, 'f', 2);
            // cout << celcius << " C = " << farenheit << " F" << Qt::endl;
            cout << msg << Qt::endl;
         }
      }
   } while (strCelcius.trimmed().length() != 0);

   return EXIT_SUCCESS;
}
