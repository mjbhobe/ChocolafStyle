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
  caseCheckBox = new QCheckBox(tr("Match &case"));
  backwardCheckBox = new QCheckBox(tr("Search &backward"));
  findButton = new QPushButton(tr("&Find"));
  findButton->setDefault(true);
  findButton->setEnabled(false);
  closeButton = new QPushButton(tr("Close"));

  // setup signals & slots
  QObject::connect(lineEdit,
                   SIGNAL(textChanged(const QString &)),
                   this,
                   SLOT(enableFindButton(const QString &)));
  QObject::connect(findButton, SIGNAL(clicked()), this, SLOT(findClicked()));
  QObject::connect(closeButton, SIGNAL(clicked()), this, SLOT(close()));

  // layout the widgets
  QHBoxLayout *topLeft = new QHBoxLayout;
  topLeft->addWidget(label);
  topLeft->addWidget(lineEdit);

  QVBoxLayout *left = new QVBoxLayout;
  left->addLayout(topLeft);
  left->addWidget(caseCheckBox);
  left->addWidget(backwardCheckBox);

  QVBoxLayout *right = new QVBoxLayout;
  right->addWidget(findButton);
  right->addWidget(closeButton);
  right->addStretch();

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
  if (backwardCheckBox->isChecked())
    emit findPrevious(text, cs);
  else
    emit findNext(text, cs);
}

void FindDialog::enableFindButton(const QString &text)
{
  findButton->setEnabled(!text.isEmpty());
}
