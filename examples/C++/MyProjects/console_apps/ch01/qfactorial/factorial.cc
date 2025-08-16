// -------------------------------------------------------------------------
// factorial.cc : calculate factorials of numbers
// In this example we make use of GNU MPZ class library
//
// @author: Manish Bhobé
// My experiments with C++ & Qt Framework
// This code is meant for learning & educational purposes only!!
// -------------------------------------------------------------------------
#include <QString>
#include <QTextStream>
#include <QtGui>
#include <gmpxx.h> // GNU arbit precision numbers
using namespace std;
#include "common_funcs.h"

QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);

/*
QTextStream &operator<<(QTextStream &ost, const mpz_class &c)
{
   QString qstr(c.get_str().c_str());
   ost << qstr;
   return ost;
}

mpz_class factorial(mpz_class &num)
{
   mpz_class ans = 1;

   for (mpz_class l = 2; l <= num; l++)
      ans *= l;
   return ans;
}
*/

void factorial(unsigned long n, mpz_t &result)
{
  mpz_set_ui(result, 1);  // result = 1
  while (n > 1) {
    mpz_mul_ui(result, result, n);  // result = result * n
    n = n-1;
  }
}

int main(void)
{
   do {
      bool ok{false};
      QString num = QInputDialog::getText(nullptr, "Factorial Calculator",
            "Enter a positive number:", QLineEdit::Normal, "", &ok);
      if (!ok || (num.trimmed().length() == 0)
         break;

      unsigned long ul = num.toULong(&ok);
      if (ok) {
        mpz_class fact = mpz_class::factorial(ul);
        cout << ul << "! = " << fact << Qt::endl;
      }
      else {
        cout << "FATAL: cannot convert " << num
          << " to unsigned long!" << Qt::endl;
        continue;
      }
   } while (true); // infinite loop: broken if you enter blank string (press Enter)

   return 0;
}
