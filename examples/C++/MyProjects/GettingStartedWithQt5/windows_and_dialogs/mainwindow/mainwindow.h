#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class QMenu;
class QAction;
class QLabel;
class QToolBar;

class MainWindow : public QMainWindow {
  Q_OBJECT

public:
  MainWindow();

private:
  void createActions();

  QLabel *m_label;
  // menus & actions
  QMenu *m_fileMenu;
  QMenu *m_helpMenu;
  QToolBar *m_toolBar;
  QAction *m_newAction;
  QAction *m_openAction;
  QAction *m_saveAction;
  QAction *m_quitAction;
  QAction *m_cancelAction;
  QAction *m_aboutAction;
  QAction *m_aboutQtAction;

private slots:
  void about();
};


#endif // __MainWindow_h__
