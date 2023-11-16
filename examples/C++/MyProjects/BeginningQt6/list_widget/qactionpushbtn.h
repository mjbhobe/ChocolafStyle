#ifndef QACTIONPUSHBTN_H
#define QACTIONPUSHBTN_H

#include <QAction>
#include <QPushButton>

class QActionPushBtn : public QPushButton {
  Q_OBJECT
public:
  QActionPushBtn(QAction *action, QWidget *parent = nullptr);
};

#endif // QACTIONPUSHBTN_H
