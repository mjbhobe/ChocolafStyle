// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_hxx__
#define __DrawWindow_hxx__

#include <QMainWindow>

class DrawWindow : public QMainWindow
{
   Q_OBJECT
 public:
   DrawWindow();

 protected:
   // operating system events
   void closeEvent(QCloseEvent *event);
   void mousePressEvent(QMouseEvent *event);
};

#endif // __DrawWindow_hxx__
