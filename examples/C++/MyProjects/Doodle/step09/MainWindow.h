// MainWindow.h - main window of app
#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class QAction;
class QMenu;
class DrawWindow;

class MainWindow : public QMainWindow
{
  Q_OBJECT
public:
  MainWindow();

public slots:
  void exitApp();
  void about();
  void doodleModified(bool);

private:
  void createActions();
  void createMenus();
  void createToolBar();
  void createStatusBar();

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

// implemented in step09.cc
MainWindow *getMainWindow();

#endif // __MainWindow_h__
