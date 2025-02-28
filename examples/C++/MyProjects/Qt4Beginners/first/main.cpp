#include "Window.h"
#include <QApplication>
#include <QFont>
#include <QPushButton>

int main(int argc, char** argv)
{
  QApplication app(argc, argv);
  app.setStyle("Fusion");
  app.setApplicationName(QString("Hello Qt %1").arg(QT_VERSION_STR));

  Window window;
  window.setFixedSize(200, 100);

  /* moved to Window class
    QPushButton* btn = new QPushButton("Hello World!", &window);
    btn->setToolTip("Qt makes C++ GUI programming easy!");
    btn->setGeometry(10, 10, 150, 30);
    QFont font("Courier 10 Pitch", 11);
    btn->setFont(font);
    btn->setIcon(QIcon::fromTheme("face-smile-big"));
        */

  window.show();

  return app.exec();
}
