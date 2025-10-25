// listDialog.cpp - ListDialog class implementation
#include "listDialog.h"
#include "editDialog.h"
#include <QDialog>
#include <QStringList>

ListDialog::ListDialog(QWidget *parent /*= nullptr*/) : QDialog(parent)
{
  ui.setupUi(this);
  // setup signals & slots
  QObject::connect(ui.addButton, SIGNAL(clicked()), this, SLOT(addItems()));
  QObject::connect(ui.editButton, SIGNAL(clicked()), this, SLOT(editItems()));
  QObject::connect(ui.deleteButton, SIGNAL(clicked()), this, SLOT(deleteItems()));
}

void ListDialog::addItems()
{
  EditDialog dlg(this);
  dlg.setWindowTitle("Add new contact");

  // call as a modal dialog
  if (dlg.exec() == QDialog::Accepted) {
    ui.list->addItem(dlg.name() + " -- " + dlg.number());
  }
}

void ListDialog::deleteItems()
{
  delete ui.list->currentItem();
}

void ListDialog::editItems()
{
  if (ui.list->currentItem()) {
    QStringList parts = ui.list->currentItem()->text().split("--");

    EditDialog dlg(this);
    dlg.setWindowTitle("Edit contact");
    dlg.setName(parts[0].trimmed());
    dlg.setNumber(parts[1].trimmed());

    if (dlg.exec() == QDialog::Accepted)
      ui.list->currentItem()->setText(dlg.name() + "--" + dlg.number());
  }
}
