// factorial.cc - calculate factorial of any +ve number
#include <gmp.h>
#include <gmpxx.h>

#include <cstdlib>
//#include <print>
#include <QtCore>

#include "common_funcs.h"

// DO NOT include <iostream>
static QTextStream cout(stdout, QIODevice::WriteOnly);
static QTextStream cerr(stderr, QIODevice::WriteOnly);
static QTextStream cin(stdin, QIODevice::ReadOnly);

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);
  QString ans{""};
  bool contd{true};

  do {
    cout << "Factorial of (press Enter to end)? " << Qt::flush;
    //std::printf("Factorial of (press Enter to end)? ");
    fflush(stdin);
    ans = cin.readLine();
    if (ans.trimmed().length() == 0)
      contd = false;
    else {
      bool ok;
      long val = ans.trimmed().toLong(&ok);
      if (!ok) {
        cerr << "Error " << ans.trimmed() << " is not numeric!" << Qt::endl;
      } else {
        mpz_class fact = mpz_class::factorial(val);
        cout << val << "! = " << fact << Qt::endl;
      }
    }
  } while (contd);

  return EXIT_SUCCESS;
}
