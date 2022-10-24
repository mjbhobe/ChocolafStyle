// splitter.cpp - illustrates using the QSplitter class
#include "HexSpinBox.h"
#include "chocolaf.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

int main(int argc, char **argv)
{
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  Chocolaf::ChocolafApp app(argc, argv);
  app.setStyle("Chocolaf");

  // create & show the GUI
  QWidget window;
  QLabel *label = new QLabel("Hex SpinBox");
  HexSpinBox *hexSpinBox = new HexSpinBox();
  QPushButton *closeBtn = new QPushButton("&Close");
  closeBtn->setDefault(true);
  QGridLayout *layout = new QGridLayout();
  layout->addWidget(label, 0, 0);
  layout->addWidget(hexSpinBox, 0, 1);
  // layout->addStretch(1, 0);
  layout->addWidget(closeBtn, 1, 1);
  window.setLayout(layout);
  window.setWindowTitle(QString("Qt %1: Splitter example").arg(QT_VERSION_STR));
  window.setWindowIcon(QIcon(":/default_app_icon.png"));
  hexSpinBox->setValue(127);

  // setup signals & slots
  QObject::connect(closeBtn, SIGNAL(clicked()), &app, SLOT(quit()));
  window.show();

  return app.exec();
}
