// -------------------------------------------------------------------------
// hello.cc: Hello World with Qt Framework (console version)
//
// @author: Manish Bhobé
// My experiments with C++, Python & the Qt Framework
// This code is meant for learning & educational purposes only!!
// -------------------------------------------------------------------------
#include <QTextStream>
#include <format>

// NOTE: do NOT include <iostream> header!!
static QTextStream cout(stdout, QIODeviceBase::WriteOnly);

int main() {
   cout << "Hello World, welcome to the Qt Framework!" << Qt::endl;
   // we can easily mix std C++ with Qt
   cout <<
      std::format("You are using Qt Framework version {}", QT_VERSION_STR).c_str()
      << Qt::endl;
   //cout << "You are using Qt Framework version " << QT_VERSION_STR << Qt::endl;

   return 0;
}
