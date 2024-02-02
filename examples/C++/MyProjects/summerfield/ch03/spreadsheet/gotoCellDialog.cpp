#include "gotocelldialog.h"
#include <QDialog>
#include <QRegularExpression>
#include <QRegularExpressionValidator>

GoToCellDialog::GoToCellDialog(QWidget *parent) : QDialog(parent)
{
  setupUi(this);
  QRegularExpression regExp("[A-Za-z][1-9][0-9]{0,2}");
  lineEdit->setValidator(new QRegularExpressionValidator(regExp, this));

  connect(okButton, SIGNAL(clicked()), this, SLOT(accept()));
  connect(cancelButton, SIGNAL(clicked()), this, SLOT(reject()));
  connect(lineEdit,
          SIGNAL(textChanged(const QString &)),
          this,
          SLOT(on_lineEdit_textChanged()));
}

void GoToCellDialog::on_lineEdit_textChanged()
{
  okButton->setEnabled(lineEdit->hasAcceptableInput());
}
