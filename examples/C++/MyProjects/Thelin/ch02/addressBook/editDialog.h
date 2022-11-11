// editDialog.h -- EditDialog class declaration
#ifndef __EditDialog_h__
#define __EditDialog_h__

#include <QDialog>
#include "ui_editdialog.h"

class EditDialog : public QDialog
{
  Q_OBJECT
public:
  EditDialog(QWidget* parent = nullptr);

  // property getters & setters
  const QString name() const;
  void setName(const QString& name);

  const QString number() const;
  void setNumber(const QString& number);

private:
  Ui::EditDialog ui;
};

#endif  // __EditDialog_h__
