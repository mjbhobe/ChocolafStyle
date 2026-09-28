// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>

class QImage;
class QColor;

class DrawWindow : public QMainWindow {
    Q_OBJECT public:
    DrawWindow();

  protected:
    // operating system events
    void closeEvent(QCloseEvent* event) override;
    void paintEvent(QPaintEvent* event) override;
    void resizeEvent(QResizeEvent* event) override;

    // event messages
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;
  private:
    // helper functions
    void drawLineTo(const QPoint &pt);
    void clearImage();
    void resizeImage(const QSize &size);

    QImage _image;
    bool _modified;

    QPoint _lastPt;
    bool _dragging;
    int _penWidth;
    QColor _penColor;
};

#endif // __DrawWindow_h__
