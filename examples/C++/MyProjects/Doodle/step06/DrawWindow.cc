// DrawWindow.cc: implements DrawWindow class
#include <QtGui>
#include <QApplication>
#include <QMessageBox>
#include <QInputDialog>
#include <QColorDialog>
#include "DrawWindow.h"
#include "Doodle.h"
#include "Line.h"
#include "chocolaf.h"

const QString AppTitle("Qt Scribble");
const QString WindowTitle = QString("Qt %1 Doodle - Step06: Drawing multiple lines").arg(QT_VERSION_STR);

DrawWindow::DrawWindow()
{
  setAttribute(Qt::WA_StaticContents);
  setWindowTitle(WindowTitle);
  _dragging = false;
  _doodle = new Doodle();
  _currLine = 0;
}

DrawWindow::~DrawWindow()
{
  delete _doodle;
}

void DrawWindow::closeEvent(QCloseEvent *event)
{
  // window is about to close, prompt user & decide if ok to quit
  // based on user's response.
  if (_doodle->modified()) {
    switch(QMessageBox::question(this, tr("Qt Scribble Tutorial"),
          tr("This will close the application.\nOk to quit now?"),
          QMessageBox::Yes|QMessageBox::No, QMessageBox::No))
    {
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

void DrawWindow::drawLineTo(const QPoint& pt)
{
  Q_ASSERT(_currLine != nullptr);
  // draw line from _lastPt to pt
  QPainter painter(&_image);
  QPen pen(_currLine->penColor(), _currLine->penWidth());
  painter.setRenderHint(QPainter::Antialiasing);
  painter.setPen(pen);
  painter.drawLine(_lastPt, pt);
  _lastPt = pt;
  update();
}

void DrawWindow::clearImage()
{
  Q_ASSERT(_doodle != nullptr);
  _doodle->clear();
  //_image.fill(qRgb(255,255,255));
  _image.fill(Chocolaf::ChocolafPalette::Window_Color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  Q_ASSERT(_doodle != nullptr);

  // check if Ctrl key is held down as left/right mouse is clicked
  Qt::KeyboardModifiers modifiers  = QApplication::queryKeyboardModifiers ();
  bool ctrlKeyIsDown = modifiers.testFlag( Qt::ControlModifier);

  qDebug() << "mousePressEvent() - CTRL key "
    << (ctrlKeyIsDown ? "IS" : "IS **NOT**")
    << " held down!";

  if (event->button() == Qt::LeftButton) {
    // left mouse button pressed
    if (ctrlKeyIsDown)
      changePenWidth();
    else {
      _currLine = _doodle->newLine();
      _lastPt = event->pos();
      _currLine->addPoint(_lastPt);
      _dragging = true;
      _doodle->setModified(true);
    }
  }
  else if (event->button() == Qt::RightButton) {
    if (ctrlKeyIsDown)
      changePenColor();
    else {
      clearImage();
      _doodle->setModified(false);
    }
  }
}

void  DrawWindow::mouseMoveEvent(QMouseEvent *event)
{
  if (event->buttons() & Qt::LeftButton && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
  }
}

void DrawWindow::mouseReleaseEvent(QMouseEvent *event)
{
  if ((event->button() == Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
    _dragging = false;
  }
}

void DrawWindow::changePenWidth()
{
  Q_ASSERT(_doodle != nullptr);
  // display message box & get width of pen
  bool ok;
  int newPenWidth = QInputDialog::getInt(this, AppTitle,
      QString("Enter new pen width:"), _doodle->penWidth(), 2, 10, 1, &ok);
  if (ok) {
    qDebug() << "New pen width selected: " << newPenWidth;
    _doodle->setPenWidth(newPenWidth);
  }
}

void DrawWindow::changePenColor()
{
  Q_ASSERT(_doodle != nullptr);
  // display standard color dialog & get new pen color
  QColor color = QColorDialog::getColor(_doodle->penColor(), this);
  if (color.isValid())
    _doodle->setPenColor(color);
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
  painter.setRenderHint(QPainter::Antialiasing);
  // we just blit the from image to device
  QRect dirtyRect = event->rect();
  painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize& newSize)
{
  if (_image.size() == newSize)
    return;
  QImage newImage(newSize, QImage::Format_RGB32);
  //newImage.fill(qRgb(255,255,255));
  newImage.fill(Chocolaf::ChocolafPalette::Window_Color);
  // draw existing image over new image
  QPainter painter(&newImage);
  painter.setRenderHint(QPainter::Antialiasing);
  painter.drawImage(QPoint(0,0), _image);
  _image = newImage;
}





