#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>
class QSpinBox;
class QSlider;
class QLabel;
class QPushButton;

class Widget : public QWidget
{
  Q_OBJECT
public:
  explicit Widget(QWidget *parent = nullptr);

signals:

private slots:
  void celciusChanged(int celcius);

private:
  QSpinBox *spinBox;
  QSlider *slider;
  QLabel *faren, *qtVer;
  QPushButton *close;

  float c2f(int celcius);
  void setupUi();
};

#endif // WIDGET_H
