#include "qactionpushbtn.h"

QActionPushBtn::QActionPushBtn(QAction *action, QWidget *parent)
    : QPushButton(parent) {
  setIcon(action->icon());
  setText(action->text());
  setToolTip(action->toolTip());
  connect(this, SIGNAL(clicked()), action, SLOT(triggered()));
}
