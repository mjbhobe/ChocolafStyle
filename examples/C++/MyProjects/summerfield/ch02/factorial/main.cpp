#include "widget.h"

#include <gmp.h>
#include <QApplication>

int main(int argc, char *argv[])
{
  QApplication app(argc, argv);
  app.setFont(QApplication::font("QMenu"));

  Widget w;
  w.show();

  return app.exec();
}
