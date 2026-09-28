// MainWindow.h - main window of app
#ifndef __MainWindow_h__
#define __MainWindow_h__

#include <QMainWindow>

class QAction;
class QMenu;
class QTimerEvent;
class DrawWindow;

class MainWindow : public QMainWindow {
   //@formatter:off
    Q_OBJECT
   //@formatter:on
  public:
    explicit MainWindow(QWidget *parent=nullptr);

  public slots:
    void exitApp();
    void about();

  private:
    void createActions();
    void createMenus();
    void createToolbar();

    // central widget
    DrawWindow* _drawWindow{nullptr};

    // actions
    QAction* fileNewAction{nullptr};
    QAction* fileOpenAction{nullptr};
    QAction* fileSaveAction{nullptr};
    QAction* fileSaveAsAction{nullptr};
    QAction* exitAction{nullptr};
    QAction* penWidthAction{nullptr};
    QAction* penColorAction{nullptr};
    QAction* aboutQtAction{nullptr};
    QAction* aboutAction{nullptr};
    // menus
    QMenu* fileMenu{nullptr};
    QMenu* optionsMenu{nullptr};
    QMenu* helpMenu{nullptr};
};

#endif // __MainWindow_h__
