// ==================================================================================
// Buttons - using push button widgets
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QPushButton>
#include <QVBoxLayout>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  QWidget widget;
  QVBoxLayout *layout = new QVBoxLayout();

  QPushButton *btn = new QPushButton(QIcon("exit.png"), "Push Me!");
  btn->setToolTip("Click button to close application");
  QObject::connect(btn, &QPushButton::clicked, &app, &QApplication::quit);

  layout->addWidget(btn);
  widget.setLayout(layout);
  widget.show();
  return app.exec();
}
