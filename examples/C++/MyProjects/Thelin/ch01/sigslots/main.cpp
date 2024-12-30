// main.cpp - driver code
#include "myclass.h"
#include <QTextStream>

QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

int main(int /*argc*/, char ** /*argv*/)
{
    QObject parent; // dummy parent
    MyClass *a, *b, *c;

    a = new MyClass("foo", &parent);
    b = new MyClass("bar", &parent);
    c = new MyClass("baz", &parent);

    QObject::connect(a, SIGNAL(textChanged(const QString &)), b, SLOT(setText(const QString &)));
    QObject::connect(b, SIGNAL(textChanged(const QString &)), c, SLOT(setText(const QString &)));
    QObject::connect(c, SIGNAL(textChanged(const QString &)), b, SLOT(setText(const QString &)));

    cout << *a << " " << *b << " " << *c << Qt::endl;

    b->setText("bug");

    cout << *a << " " << *b << " " << *c << Qt::endl;

    return 0;
}
