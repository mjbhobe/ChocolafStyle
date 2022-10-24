// splitter.cpp - illustrates using the QSplitter class
#include "chocolaf.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

QString english = QString(
  "My child, my sister,\nthink of the sweetness\n"
  "of going there to live together!\n"
  "To love at leasure\nto love and to die\nin a country that is an image of you");
QString french = QString(
  "Mon enfant, ma soeur\npense à la douceur\n"
  "d'y aller vivre ensemble!\nAimer à loisir\naimer et mourir\ndans un pays qui est ton image");
QString german = QString("Mein Kind, meine Schwester,\ndenken Sie an die Süße\ndorthin zu gehen, "
                         "um zusammen zu leben!\nIn Ruhe lieben\nzu lieben und "
                         "zu sterben\nin einem Land, das ein Abbild von dir ist");

int main(int argc, char **argv)
{
  Chocolaf::ChocolafApp::setupForHighDpiScreens();
  Chocolaf::ChocolafApp app(argc, argv);
  app.setStyle("Chocolaf");

  // create & show the GUI
  QTextEdit *frenchEdit = new QTextEdit();
  QTextEdit *englishEdit = new QTextEdit();
  QTextEdit *germanEdit = new QTextEdit();
  frenchEdit->setText(french);
  englishEdit->setText(english);
  germanEdit->setText(german);

  QSplitter splitter = QSplitter(Qt::Horizontal);
  splitter.addWidget(frenchEdit);
  splitter.addWidget(englishEdit);
  splitter.addWidget(germanEdit);

  Chocolaf::centerOnScreenWithSize(splitter, 0.50, 0.15);
  splitter.setWindowTitle(QString("Qt %1: Splitter example").arg(QT_VERSION_STR));
  splitter.setWindowIcon(QIcon(":/default_app_icon.png"));
  splitter.show();

  return app.exec();
}
