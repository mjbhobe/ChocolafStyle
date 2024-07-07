// ----------------------------------------------------------
// stringdemo.cc - illustrates use of QString class
//
// @author: Manish Bhobe
// My experiments with C++ & Qt. Use at your own risk!
// This code is intended for illustration purposes only
// ----------------------------------------------------------
#include <cstdio>
#include <QString>
#include <QDebug>
#include <QTextStream>

QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);
QTextStream cerr(stdout, QIODeviceBase::WriteOnly);

int main(void) {
   QString s1("This "), s2("is a "), s3("concatenated QString");
   auto s4 = s1 + s2 + s3;
   cout << s4 << Qt::endl;
   cout << "Length of string: " << s4.length() << Qt::endl;
   cout << "Enter a sentence with whitespaces: " << Qt::flush;
   auto s5 = cin.readLine();
   cout << "You entered: " << s5 << Qt::endl;

   // print various data types
   const auto SPACE = ' ';

   cout << "Displaying integers in various formats" << Qt::endl;
   int num1{1234}, num2{2345};
   cout << num2 << SPACE << Qt::oct << num2 << " (oct)" << SPACE
      << Qt::hex << num2 << " (hex)" << SPACE 
      << Qt::dec << num2 << " (dec)" << Qt::endl;

   cout << "Displaying floats in various formats" << Qt::endl;
   double dub{123.456};
   cout << dub << SPACE << Qt::forcesign << dub << SPACE
      << Qt::forcepoint << dub << Qt::endl;
   cout << dub << SPACE << Qt::scientific << dub << SPACE
      << Qt::noforcesign << dub << Qt::endl;

   qDebug() << "Here is a message with " << dub << "in it.";
   qDebug("Here is a message with integer %d in it", num1);


   return 0;
}

