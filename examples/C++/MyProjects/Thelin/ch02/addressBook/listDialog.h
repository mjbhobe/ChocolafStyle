// listDialog.h - class for the main window
#ifndef __ListDialog_h__
#define __ListDialog_h__

#include <QDialog>
#include "ui_listdialog.h"

class ListDialog : public QDialog
{
  Q_OBJECT
public:
  ListDialog(QWidget *parent = nullptr);
private slots:
  void addItems();
  void editItems();
  void deleteItems();

private:
  // the UI that this envelopes
  Ui::ListDialog ui;
};

#endif  // __ListDialog_h__

