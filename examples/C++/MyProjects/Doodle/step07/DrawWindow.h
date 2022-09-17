// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>

// pre-declarations
class QImage;
class QColor;
class QAction;
class QMenu;
class Line;
class Doodle;
class QToolBar;

class DrawWindow  : public QMainWindow {
   Q_OBJECT
      public:
               DrawWindow();
   ~DrawWindow();
 protected:
   // operating system events
   void closeEvent(QCloseEvent *event);
   void paintEvent(QPaintEvent *event);
   void resizeEvent(QResizeEvent *event);

   void mousePressEvent(QMouseEvent *event);
   void mouseMoveEvent(QMouseEvent *event);
   void mouseReleaseEvent(QMouseEvent *event);
 private slots:
   // action response slots
   void fileNew();
   void fileOpen();
   void fileSave();
   void fileSaveAs();
   void exitApp();
   void changePenWidth();
   void changePenColor();
   void about();

 private:
   void drawLineTo(const QPoint& pt);
   void clearImage();
   void resizeImage(const QSize& size);
   void createActions();
   void createMenus();
   void createToolbar();
   bool canClose();

      // members
   QImage _image;
   QPoint _lastPt;
   bool _dragging;
   Doodle *_doodle;
   Line *_currLine;

      // actions
   QAction *fileNewAction;
   QAction *fileOpenAction;
   QAction *fileSaveAction;
   QAction *fileSaveAsAction;
   QAction *exitAction;
   QAction *penWidthAction;
   QAction *penColorAction;
   QAction *aboutQtAction;
   QAction *aboutAction;
   // menus
   QMenu *fileMenu;
   QMenu *optionsMenu;
   QMenu *helpMenu;
   QToolBar *toolbar;
};


#endif  // __DrawWindow_h__
