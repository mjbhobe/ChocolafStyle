#ifndef __GoToCellDialog_h__
#define __GoToCellDialog_h__

#include <QDialog>
#include "ui_gotocelldialog.h"

class GoToCellDialog : public QDialog, public Ui::GoToCellDialog
{
    Q_OBJECT
  public:
    GoToCellDialog(QWidget *parent = nullptr);
  private slots:
    void on_lineEdit_textChanged();
};

#endif // __GoToCellDialog_h__
