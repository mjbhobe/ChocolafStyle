// DrawWindow.h: the main drawing window
#ifndef __DrawWindow_h__
#define __DrawWindow_h__

#include <QMainWindow>
#include <QWidget>

class QImage;

class DrawWidget : public QWidget {
    Q_OBJECT
  public:
    DrawWidget(QWidget *parent=nullptr);
    bool isModified() const { return _modified; }

  protected:
    // operating system events
    // void closeEvent(QCloseEvent *event);
    void mousePressEvent(QMouseEvent*event) override;
    void paintEvent(QPaintEvent *event) override;
    void resizeEvent(QResizeEvent *event) override;
  private:
    // our custom functions
    void drawPoint(const QPoint &pt);
    void clearImage();
    void resizeImage(const QSize &size);

    QImage _image;
    bool _modified;
};

class DrawMainWindow : public QMainWindow {
  private:
    DrawWidget *_drawWidget;
  public:
    DrawMainWindow(DrawWidget *win);
  protected:
    // OS events
    void closeEvent(QCloseEvent *event) override;
};

#endif // __DrawWindow_h__
