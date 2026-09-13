#include <QApplication>
#include <QLabel>
#include <QVBoxLayout>
#include <format>
#include <string>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  QWidget widget;

  QVBoxLayout *layout = new QVBoxLayout;
  std::string str = std::format("Hello Qt {} World!", QT_VERSION_STR);
  QLabel *label = new QLabel(QString::fromStdString(str));
  layout->addWidget(label);
  widget.setLayout(layout);
  widget.show();

  return app.exec();
}
