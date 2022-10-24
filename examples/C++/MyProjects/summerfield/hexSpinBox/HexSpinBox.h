#ifndef HEXSPINBOX_H
#define HEXSPINBOX_H

#include <QSpinBox>

class QRegularExpressionValidator;

class HexSpinBox : public QSpinBox
{
  Q_OBJECT
public:
  HexSpinBox(QWidget* parent = nullptr);

protected:
  QValidator::State validate(QString& text, int& pos) const;
  QString textFromValue(int value) const;
  int valueFromText(const QString& text) const;

private:
  QRegularExpressionValidator* validator;
};

#endif // HEXSPINBOX_H
