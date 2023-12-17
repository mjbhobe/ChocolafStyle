// editDialog.cpp - EditDialog class implementation
#include <QObject>
#include <QString>
#include "editDialog.h"

EditDialog::EditDialog(QWidget* parent /*= nullptr*/) : QDialog(parent)
{
  ui.setupUi(this);
}

const QString EditDialog::name() const
{
  return ui.nameEdit->text().replace("--","").trimmed();
}

void EditDialog::setName(const QString& name)
{
  ui.nameEdit->setText(name);
}

const QString EditDialog::number() const
{
  return ui.numberEdit->text().replace("--","").trimmed();
}

void EditDialog::setNumber(const QString& number)
{
  ui.numberEdit->setText(number);
}




