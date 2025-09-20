// -------------------------------------------------------------------------
// hello.cc: Hello World with Qt Framework (console version)
//
// @author: Manish Bhobé
// My experiments with C++, Python & the Qt Framework
// This code is meant for learning & educational purposes only!!
// -------------------------------------------------------------------------
#include <QTextStream>

static QTextStream cout(stdout, QIODeviceBase::WriteOnly);

int main() {
   cout << "Hello World, welcome to the Qt Framework!" << Qt::endl;
   cout << "You are using Qt Framework version " << QT_VERSION_STR << Qt::endl;

   return 0;
}
