#include "argparse/argparse.hpp"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <filesystem>
#include <fmt/core.h>

#include "ImageViewer.h"
#include "common_funcs.h"
namespace fs = std::filesystem;

const QString AppTitle("Qt with OpenCV ImageViewer");
static QTextStream cerr(stderr, QIODevice::WriteOnly);

// define expected command line args
// @see: https://github.com/morrisfranken/argparse
struct MyArgs : public argparse::Args {
  // -i | --image <image_path>
  std::string &image_path =
      kwarg("i,image", "Full path to image file to display.").set_default("");
};

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  QFile f(":chocolaf/chocolaf.css");

  if (!f.exists()) {
    printf("Unable to open stylesheet!");
  } else {
    f.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&f);
    app.setStyleSheet(ts.readAll());
  }
  app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

  // parse the command line params
  MyArgs args = argparse::parse<MyArgs>(argc, argv, /* raise_on_error */ true);

  ImageViewer w;
  if ((args.image_path != "")) {
    if (fs::exists(args.image_path)) {
      w.loadImage(QString(args.image_path.c_str()));
      w.updateActions();
    } else {
      cerr << "WARNING: " << args.image_path.c_str() << " - path does not exist!"
           << Qt::endl;
    }
  }
  w.show();

  return app.exec();
}
