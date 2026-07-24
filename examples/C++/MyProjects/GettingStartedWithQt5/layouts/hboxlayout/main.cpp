// ==================================================================================
// HBox Layout - laying out widgets in a horizontal box layout
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  // create our widgets
  QWidget widget{};
  widget.setWindowTitle("Qt Layouts | QHBoxLayout");

  QLineEdit *txtUrl = new QLineEdit();
  txtUrl->setPlaceholderText(
      "Enter URL to export (e.g. https://youdomain.com/items");
  txtUrl->setFixedWidth(400); // make it this long & non-resizeable
  QPushButton *exportBtn = new QPushButton("Export");

  // layout our widgets
  QHBoxLayout *hbox = new QHBoxLayout();
  hbox->addWidget(txtUrl);
  hbox->addWidget(exportBtn);
  widget.setLayout(hbox);

  // show our "main" widget
  widget.show();
  return app.exec();
}
