// MainWindow.h - main window of app
#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class QAction;
class QMenu;
class QTimerEvent;
class DrawWindow;

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    MainWindow();

  public slots:
    void exitApp();
    void about();

  private:
    void createActions();
    void createMenus();
    void createToolbar();

    // central widget
    DrawWindow *_drawWindow;

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
};

    

    


#endif // __MainWindow_h__
