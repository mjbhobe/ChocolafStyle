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

extern const QString AppTitle;
extern const QString WindowTitle;

class DrawWindow  : public QMainWindow {
    Q_OBJECT
  public:
    DrawWindow();
    ~DrawWindow();
    void resizeImage(const QSize& size, bool force=false);
  protected:
    // operating system events
    void closeEvent(QCloseEvent *event);
    void paintEvent(QPaintEvent *event);
    void resizeEvent(QResizeEvent *event);

    void mousePressEvent(QMouseEvent *event);
    void mouseMoveEvent(QMouseEvent *event);
    void mouseReleaseEvent(QMouseEvent *event);
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
    bool _dragging;
    Doodle *_doodle;
    Line *_currLine;
};


#endif  // __DrawWindow_h__
