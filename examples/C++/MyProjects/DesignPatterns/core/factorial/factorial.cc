// factorial.cc - calculate factorial of any +ve number
//
// NOTE: we are using the gmp/gmpxx libraries to make that possible.
// For a perspective on why we are using gmp/gmpxx
// a> because it can handle any arbit precision integers
// b> Standard C++ will max out at max value of unsigned long long, which
// is roughly 18,446,744,073,709,551,615 (which is no more than 20!)
// clang++/g++ extensions, offer __int128 data types, unsigned __int128
// will max out at 34!

// @author: Manish Bhobe
// My experiments with C++/STL and Qt Framework
// Code is shared for learning purposes only!
// ---------------------------------------------------------------------
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
