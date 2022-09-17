// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>
#include <QWidget>

class QImage;

class DrawWindow : public QWidget
{
   Q_OBJECT
 public:
   DrawWindow();
   bool isModified() const { return _modified; }

 protected:
   // operating system events
   // void closeEvent(QCloseEvent *event);
   void mousePressEvent(QMouseEvent *event);
   void paintEvent(QPaintEvent *event);
   void resizeEvent(QResizeEvent *event);

 private:
   // our custom functions
   void drawPoint(const QPoint &pt);
   void clearImage();
   void resizeImage(const QSize &size);

   QImage _image;
   bool _modified;
};

class DrawMainWindow : public QMainWindow
{
 private:
   DrawWindow *_drawWindow;

 public:
   DrawMainWindow(DrawWindow *win) : _drawWindow(win) {}

 protected:
   // OS events
   void closeEvent(QCloseEvent *event);
};

#endif // __DrawWindow_h__
