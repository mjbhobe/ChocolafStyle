#include "argparse/argparse.hpp"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>
#include <cstdlib>
#include <filesystem>
#include <fmt/core.h>

#include "ImageEditor.h"
#include "chocolaf.h"
#include "common_funcs.h"

namespace fs = std::filesystem;

const QString AppTitle("Qt with OpenCV ImageEditor");

// define command line arguments
// @see: https://github.com/morrisfranken/argparse
struct MyArgs : public argparse::Args {
    // -i | --image <image path>
    std::string& image_path = kwarg("i,image", "Full path to the image file to display.").set_default("");
};

int main(int argc, char** argv)
{
    /* QApplication app(argc, argv);
    QCoreApplication::setAttribute(Qt::AA_DisableHighDpiScaling);
    if (qgetenv("QT_FONT_DPI").isEmpty()) {
      qputenv("QT_FONT_DPI", "96");
    } */
    //  Chocolaf::ChocolafApp::setupForHighDpiScreens();
    Chocolaf::ChocolafApp app(argc, argv);
    //  app.setStyle("Chocolaf");
    // QApplication app(argc, argv);
    app.setStyle("Fusion");
    app.setApplicationName(app.translate("main", AppTitle.toStdString().c_str()));

    // parse out the command line arguments
    bool hasImageToOpen = false;
    QString imagePath { "" };
    /* MyArgs args = argparse::parse<MyArgs>(argc, argv);
    fs::path p = args.image_path;
    if ((args.image_path != "") && fs::exists(p)) {
        hasImageToOpen = true;
        imagePath = QString::fromStdString(p.string());
        qDebug() << "Will open image " << imagePath << " at start!";
    }*/

    /* QFile f(":chocolaf/chocolaf.css");

    if (!f.exists()) {
      printf("Unable to open stylesheet!");
    } else {
      f.open(QFile::ReadOnly | QFile::Text);
      QTextStream ts(&f);
      app.setStyleSheet(ts.readAll());
    } */

    ImageEditor w;
    if (hasImageToOpen) {
        if (w.loadImage(imagePath))
            w.updateActions();
    }
    w.show();

    return app.exec();
}
