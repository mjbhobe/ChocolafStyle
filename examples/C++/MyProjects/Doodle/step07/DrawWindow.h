// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>

// pre-declarations
class QImage;
class QColor;
class Line;
class Doodle;

class DrawWindow : public QMainWindow {
  //@formatter:off
    Q_OBJECT
  //@formatter:on
  public:
    DrawWindow();
    ~DrawWindow();

  protected:
    // operating system events
    void closeEvent(QCloseEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;

  private:
    void drawLineTo(const QPoint& pt);
    void clearImage();
    void resizeImage(const QSize& size);
    void changePenWidth();
    void changePenColor();

    QImage _image;

    QPoint _lastPt;
    bool _dragging;
    Doodle* _doodle;
    Line* _currLine;
};

#endif // __DrawWindow_h__
