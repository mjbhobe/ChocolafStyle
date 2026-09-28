// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QWidget>

// pre-declarations
class QImage;
class QColor;
class QAction;
class QMenu;
class Line;
class Doodle;


class DrawWindow : public QWidget {
   //@formatter:off
   Q_OBJECT
    //@formatter:on
  public:
    explicit DrawWindow(QWidget *parent=nullptr);
    ~DrawWindow();

    void resizeImage(const QSize& size, bool force = false);

  protected:
    // operating system events
    void closeEvent(QCloseEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;

  private slots:
    // action response slots
    void fileNew();
    void fileOpen();
    void fileSave();
    void fileSaveAs();
    void changePenWidth();
    void changePenColor();

  private:
    void drawLineTo(const QPoint& pt);
    void clearImage();
    bool canClose();

    // members
    QImage _image;
    QPoint _lastPt;
    bool _dragging{false};
    Doodle* _doodle{nullptr};
    Line* _currLine{nullptr};
};

#endif // __DrawWindow_h__
