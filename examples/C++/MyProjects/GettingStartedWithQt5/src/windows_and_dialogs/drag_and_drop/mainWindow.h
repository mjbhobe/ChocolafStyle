#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class DragTextEdit;

class MainWindow : public QMainWindow {
    Q_OBJECT

  public:
    MainWindow(QWidget* parent = 0);

  private
  slots :
    void updateStatusBar();

  private:
    DragTextEdit* slateDragTextEdit;
};

#endif  // __MainWindow_h__
