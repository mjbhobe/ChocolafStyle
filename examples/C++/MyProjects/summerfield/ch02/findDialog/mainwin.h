#ifndef MAINWIN_H
#define MAINWIN_H

#include <QWidget>

class QPushButton;

class MainWin : public QWidget
{
  Q_OBJECT
public:
  explicit MainWin(QWidget *parent = nullptr);

signals:

private slots:
  void findDialogButtonClicked();
  void gotoCellDialogButtonClicked();

private:
  QPushButton *callFindDialog;
  QPushButton *callGotoCellDialog;
};

#endif // MAINWIN_H
