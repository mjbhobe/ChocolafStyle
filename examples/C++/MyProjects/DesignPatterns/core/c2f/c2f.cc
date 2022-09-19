// c2f.cc - convert celcius temp to farenheit
#include "common_funcs.h"
#include <QtCore>
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

  do {
    cout << "Celcius temp (enter to quit)? " << Qt::flush;
    strCelcius = cin.readLine();
    if (strCelcius.trimmed().length() != 0) {
      celcius = strCelcius.toFloat(&ok);
      if (!ok) {
        cerr << "FATAL " << strCelcius << " - not numeric!" << Qt::endl;
      } else {
        farenheit = (celcius * (9.0f / 5.0f)) + 32.0f;
        cout << celcius << " C = " << farenheit << " F" << Qt::endl;
      }
    }
  } while (strCelcius.trimmed().length() != 0);

  return EXIT_SUCCESS;
}
