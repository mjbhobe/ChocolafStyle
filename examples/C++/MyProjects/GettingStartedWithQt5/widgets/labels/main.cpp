// ==================================================================================
// Labels with very long text
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QDebug>
#include <QGuiApplication>
#include <QLabel>
#include <QPaintDevice>
#include <QScreen>
#include <QVBoxLayout>
#include <print>

double pixelsToPoints(double pixels, const QPaintDevice *device = nullptr)
{
  double dpi = 0;
  if (device) {
    dpi = device->logicalDpiY();
  }
  else if (QScreen *screen = QGuiApplication::primaryScreen()) {
    dpi = screen->logicalDotsPerInchY();
  }

  double points = dpi > 0 ? (pixels * 72.0) / dpi : pixels;
  std::println("{} pixels is {:.2f} points", pixels, points);
  // qDebug() << pixels << " pixels is " << points << " points";
  return points;
}


int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  QWidget widget;
  QVBoxLayout *layout = new QVBoxLayout();

  // C++ 11 onwards, you can specify a very long multi-line
  // string this way (using R("multi line string..."))
  QString very_long_string = R"(
    'What do you know about this business?' the
    King said to Alice.\n'Nothing,' said Alice.\n'Nothing whatever?' persisted
    the King.\n'Nothing whatever,' said Alice."
  )";

  QLabel *label = new QLabel(very_long_string);
  label->setAlignment(
      Qt::AlignmentFlag::AlignHCenter | Qt::AlignmentFlag::AlignVCenter);
  // also set a custom font
  label->setFont(QFont("CodeNewRoman Nerd Font", pixelsToPoints(16)));

  layout->addWidget(label);
  widget.setLayout(layout);
  widget.show();
  return app.exec();
}
