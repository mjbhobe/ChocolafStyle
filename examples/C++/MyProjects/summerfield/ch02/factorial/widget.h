#ifndef WIDGET_H
#define WIDGET_H

#include <QWidget>

class QLineEdit;
class QTextEdit;
class QPushButton;
class QLabel;

class Widget : public QWidget
{
  Q_OBJECT
private:
  QLabel *label;
  QLineEdit *number;
  QPushButton *calculate;
  QPushButton *quit;
  QTextEdit *factorial;
  void setupUi();

public:
  Widget(QWidget *parent = nullptr);
  ~Widget();

private slots:
  void calculateFactorial();
};
#endif // WIDGET_H
