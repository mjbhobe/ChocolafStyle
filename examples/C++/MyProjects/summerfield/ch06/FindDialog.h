// FindDialog.h - using Grid Layout
#ifndef __FindDialog_h__
#define __FindDialog_h__

#include <QObject>
#include <QWidget>
#include <QDialog>

class QLabel;
class QLineEdit;
class QCheckBox;
class QTableWidget;
class QPushButton;

class FindDialog : public QDialog
{
      Q_OBJECT
   public:
      FindDialog(QWidget *parent=nullptr);
   private:
      QLabel *namedLabel,*lookInLabel, *messageLabel;
      QLineEdit *namedLineEdit, *lookInLineEdit;
      QTableWidget *tableWidget;
      QCheckBox *subfoldersCheckBox;
      QPushButton *findButton, *stopButton, *closeButton, *helpButton;

      void setupUi();
};

#endif   // __FindDialog_h__
