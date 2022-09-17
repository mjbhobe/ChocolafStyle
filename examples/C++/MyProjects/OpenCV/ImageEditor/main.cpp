#include <QtCore>
#include <QtGui>
#include <QtWidgets>

#include "ImageEditor.h"
#include "common_funcs.h"

const QString AppTitle("Qt with OpenCV ImageEditor");

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  QFile f(":chocolaf/chocolaf.css");

  if (!f.exists()) {
    printf("Unable to open stylesheet!");
  }
  else {
    f.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&f);
    app.setStyleSheet(ts.readAll());
  }
  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  ImageEditor w;
  w.show();

  return app.exec();
}
