// ch02/findDialog/findDialog.cc
#include "findDialog.h"
#include <QCheckBox>
#include <QDialog>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>

FindDialog::FindDialog(QWidget *parent /*=nullptr*/) : QDialog(parent)
{
  label = new QLabel(tr("Find &what:"));
  lineEdit = new QLineEdit;
  label->setBuddy(lineEdit);
  lineEdit->setMinimumWidth(250);
  caseCheckBox = new QCheckBox(tr("Match &case"));
  backwardCheckBox = new QCheckBox(tr("Search &backward"));
  wholeWordsCheckBox = new QCheckBox(tr("W&hole words only"));
  findButton = new QPushButton(tr("&Find"));
  findButton->setDefault(true);
  findButton->setEnabled(false);
  closeButton = new QPushButton(tr("Close"));

  // setup signals & slots
  QObject::connect(lineEdit, SIGNAL(textChanged(const QString &)), this,
                   SLOT(enableFindButton(const QString &)));
  QObject::connect(findButton, SIGNAL(clicked()), this, SLOT(findClicked()));
  QObject::connect(closeButton, SIGNAL(clicked()), this, SLOT(close()));

  // layout the widgets
  QHBoxLayout *topLeft = new QHBoxLayout;
  topLeft->addWidget(label);
  topLeft->addWidget(lineEdit);

  QHBoxLayout *search1 = new QHBoxLayout;
  search1->addWidget(caseCheckBox);
  search1->addWidget(wholeWordsCheckBox);

  QVBoxLayout *checkLayout = new QVBoxLayout;
  checkLayout->addLayout(search1);
  checkLayout->addWidget(backwardCheckBox);

  QVBoxLayout *left = new QVBoxLayout;
  left->addLayout(topLeft);
  left->addLayout(checkLayout);

  QVBoxLayout *right = new QVBoxLayout;
  right->addWidget(findButton);
  right->addWidget(closeButton);
  // right->addStretch();

  QHBoxLayout *main = new QHBoxLayout;
  main->addLayout(left);
  main->addLayout(right);
  setLayout(main);

  setWindowTitle(tr("Find"));
  setFixedHeight(sizeHint().height());
}

void FindDialog::findClicked()
{
  QString text = lineEdit->text();
  Qt::CaseSensitivity cs = caseCheckBox->isChecked() ? Qt::CaseSensitive : Qt::CaseInsensitive;
  bool wwo = wholeWordsCheckBox->isChecked();
  if (backwardCheckBox->isChecked())
    emit findPrevious(text, cs, wwo);
  else
    emit findNext(text, cs, wwo);
}

void FindDialog::enableFindButton(const QString &text)
{
  findButton->setEnabled(!text.isEmpty());
}
