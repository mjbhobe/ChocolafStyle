// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_hxx__
#define __DrawWindow_hxx__

#include <QMainWindow>

class DrawWidget : public QMainWindow
{
  Q_OBJECT
public:
  DrawWidget(QWidget *parent=nullptr);

protected:
  // operating system events
  void closeEvent(QCloseEvent *event) override;
  void paintEvent(QPaintEvent *event) override;
  void mousePressEvent(QMouseEvent *event) override;
};

#endif // __DrawWindow_hxx__
