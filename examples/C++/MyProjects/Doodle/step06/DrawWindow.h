// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>

// pre-declarations
class QImage;
class QColor;
class Line;
class Doodle;

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

	private:
		void drawLineTo(const QPoint& pt);	
    void clearImage();
    void resizeImage(const QSize& size);
    void changePenWidth();
    void changePenColor();

    QImage _image;

    QPoint _lastPt;
    bool _dragging;
    Doodle *_doodle;
    Line *_currLine;
};


#endif  // __DrawWindow_h__
