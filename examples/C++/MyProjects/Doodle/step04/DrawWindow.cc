// DrawWindow.cc: implements DrawWindow class

#include "DrawWindow.h"
#include "chocolaf.h"
#include <QMessageBox>
#include <QtGui>

static const QString AppTitle = {"Qt Scribble"};
static const QString WindowTitle =
    QString("Qti %1 Scribble - Step04: Drawing Lines").arg(QT_VERSION_STR);

DrawWindow::DrawWindow()
{
  setAttribute(Qt::WA_StaticContents);
  setWindowTitle(WindowTitle);
  _modified = false;
  _dragging = false;
  _penWidth = 3;
  _penColor = qRgb(0, 0, 255);
}

void DrawWindow::closeEvent(QCloseEvent *event)
{
  // window is about to close. Prompt the user and ask them
  // what they would like to do.
  if (_modified) {
    switch (QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                                  tr("This will close the application.\nOk to quit now?"),
                                  QMessageBox::Yes | QMessageBox::No, QMessageBox::No)) {
      case QMessageBox::Yes:
        // ok to quit
        event->accept();
        break;
      default:
        // don't quit yet
        event->ignore();
    }
  }
}

void DrawWindow::drawLineTo(const QPoint &pt)
{
  // draw line from _lastPt to pt
  QPainter painter(&_image);
  painter.setRenderHint(QPainter::Antialiasing, true);
  QPen pen(_penColor, _penWidth);
  painter.setPen(pen);
  painter.drawLine(_lastPt, pt);
  _lastPt = pt;
  update();
}

void DrawWindow::clearImage()
{
  //_image.fill(qRgb(255, 255, 255));
  _image.fill(Chocolaf::ChocolafPalette::Window_Color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  if (event->button() == Qt::LeftButton) {
    // left mouse button pressed
    clearImage();
    _lastPt = event->pos();
    _dragging = true;
    _modified = true;
  } else if (event->button() == Qt::RightButton) {
    clearImage();
    _modified = false;
  }
}

void DrawWindow::mouseMoveEvent(QMouseEvent *event)
{
  if (event->buttons() & Qt::LeftButton && _dragging)
    drawLineTo(event->pos());
}

void DrawWindow::mouseReleaseEvent(QMouseEvent *event)
{
  if ((event->button() & Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _dragging = false;
  }
}

void DrawWindow::resizeEvent(QResizeEvent *event)
{
  if (width() > _image.width() || height() > _image.height()) {
    int newWidth = qMax(width(), _image.width());
    int newHeight = qMax(height(), _image.height());
    resizeImage(QSize(newWidth, newHeight));
    update();
  }
  QWidget::resizeEvent(event);
}

void DrawWindow::paintEvent(QPaintEvent *event)
{
  QPainter painter(this);
  QRect dirtyRect = event->rect();
  painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize &newSize)
{
  if (_image.size() == newSize)
    return;

  QImage newImage(newSize, QImage::Format_RGB32);
  // newImage.fill(qRgb(255, 255, 255));
  newImage.fill(Chocolaf::ChocolafPalette::Window_Color);

  // draw existing image over new image
  QPainter painter(&newImage);
  painter.drawImage(QPoint(0, 0), _image);
  _image = newImage;
}
