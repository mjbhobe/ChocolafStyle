// ==================================================================================
// Hello World - basic Qt Application
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QLabel>
#include <QVBoxLayout>
#include <format>
#include <string>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  // build the GUI
  QWidget widget;
  QVBoxLayout *layout = new QVBoxLayout();

  std::string hello_qt =
      std::format("Hello World! Welcome to Qt {}", QT_VERSION_STR);
  QLabel *label = new QLabel(QString::fromStdString(hello_qt));
  label->setStyleSheet("QLabel:hover { color: rgb(60, 179, 113)}");

  layout->addWidget(label);
  widget.setLayout(layout);
  widget.show();

  return app.exec();
}
