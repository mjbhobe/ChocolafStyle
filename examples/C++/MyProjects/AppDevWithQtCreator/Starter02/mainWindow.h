// mainWindow.h - header file for main window
#ifndef __mainWindow_h__
#define __mainWindow_h__

#include <QMainWindow>
#include "Counter.h"

namespace Ui {
  class MainWindow;
}

class QPushButton;
class QLabel;

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;
  private slots:
    void onClose();
    void onCounterBtnClicked();
  private:
    Ui::MainWindow *ui;
    Counter *counter;
    QLabel *helloLabel, *counterLabel;
    QPushButton *closeBtn, *counterPlusBtn, *counterMinusBtn;
};


#endif // __mainWindow_h__
