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

class DrawWindow : public QMainWindow {
  //@formatter:off
  Q_OBJECT
  //@formatter:on
public:
    explicit DrawWindow(QWidget *parent=nullptr);
    ~DrawWindow();

  protected:
    // operating system events
    void closeEvent(QCloseEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;
    void changeEvent(QEvent *event) override;

    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;

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
    void updateActionIcons();

    // members
    QImage _image;
    QPoint _lastPt;
    bool _dragging{false};
    Doodle* _doodle{nullptr};
    Line* _currLine{nullptr};

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
    QToolBar* toolbar{nullptr};
};

#endif // __DrawWindow_h__
