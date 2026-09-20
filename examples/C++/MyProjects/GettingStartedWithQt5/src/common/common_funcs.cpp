#include "common_funcs.h"
#include <QTextStream>
#include <QString>

#ifndef _MSC_VER
#include <gmpxx.h> // GNU arbit precision numbers

QTextStream& operator<<(QTextStream& ost, const mpz_class& c)
{
  QString qstr(c.get_str().c_str());
  ost << qstr;
  return ost;
}
#endif
