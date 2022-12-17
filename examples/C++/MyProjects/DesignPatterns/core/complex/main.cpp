#include "complex.h"
#include <QCoreApplication>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);

   // constructors
   Complex c(3.5, 4.76); // default constructor
   cout << c << Qt::endl;
   Complex c1(67.65, -84.76); // default constructor
   cout << c1 << Qt::endl;

   return EXIT_SUCCESS;
}