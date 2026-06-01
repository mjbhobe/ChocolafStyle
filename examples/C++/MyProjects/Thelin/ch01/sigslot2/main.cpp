// main.cpp - driver code
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include "chocolaf.h"
#include "myclass.h"

int main(int argc, char **argv)
{
  // Chocolaf::ChocolafApp::setupForHighDpiScreens();
  // Chocolaf::ChocolafApp app(argc, argv);
  // app.setStyle("Chocolaf");
  QApplication app(argc, argv);

  // create the GUI
  QWidget window;
  window.setWindowTitle("Qt Signal Slots");
  QLineEdit *lineEdit = new QLineEdit();
  QLabel *label       = new QLabel();

  QVBoxLayout *layout = new QVBoxLayout();
  layout->addWidget(lineEdit);
  layout->addWidget(label);
  window.setLayout(layout);

  // bridge class
  MyClass *bridge = new MyClass("", &app);
  // setup signals & slots
  QObject::connect(lineEdit, SIGNAL(textChanged(const QString &)), bridge, SLOT(setText(const QString &)));
  QObject::connect(bridge, SIGNAL(textChanged(const QString &)), label, SLOT(setText(const QString &)));
  window.show();

  QStringList items;
  items << "If Manish"
        << "can code"
        << "in C++"
        << "with Qt, so"
        << "can you!";
  auto text = items.join(" ");
  // will trigger the above sig/slot chain
  lineEdit->setText(text);

  return app.exec();
}
