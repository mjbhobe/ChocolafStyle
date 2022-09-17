// DrawWindow.cc: implements DrawWindow class
#include <QtGui>
#include <QApplication>
#include <QMessageBox>
#include <QInputDialog>
#include <QColorDialog>
#include <QFileDialog>
#include <QMessageBox>
#include "DrawWindow.h"
#include "Doodle.h"
#include "Line.h"
#include "chocolaf.h"

const QString ScribbleFiles("Qt Scribble Files (*.qscb)");

DrawWindow::DrawWindow()
{
  setAttribute(Qt::WA_StaticContents);

  _dragging = false;
  _doodle = new Doodle();
  _currLine = 0;
}

DrawWindow::~DrawWindow()
{
  delete _doodle;
}


bool DrawWindow::canClose()
{
  if (_doodle->modified()) {
    switch(QMessageBox::question(this, tr("Qt Scribble Tutorial"), 
        tr("The doodle has changed. Save changes to doodle now?"),
        QMessageBox::Yes|QMessageBox::No|QMessageBox::Cancel, QMessageBox::No))
    {
      case QMessageBox::Yes:
        // save doodle & quit
        fileSave(); 
        return true;
      case QMessageBox::No:
        // quit without saving
        return true;
      default:
        // don't quit yet!
        return false;
    }
  }
  return true;  // if not modified, I canClose()
}

void DrawWindow::closeEvent(QCloseEvent *event)
{
  if (canClose())
    event->accept();
  else
    event->ignore();
}

void DrawWindow::drawLineTo(const QPoint& pt)
{
  Q_ASSERT(_currLine != 0);
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
  Q_ASSERT(_doodle != 0);
  _doodle->clear();
  //_image.fill(qRgb(255,255,255));
  _image.fill(Chocolaf::ChocolafPalette::Window_Color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  Q_ASSERT(_doodle != 0);

  // check if Ctrl key is held down as left/right mouse is clicked
  Qt::KeyboardModifiers modifiers  = QApplication::queryKeyboardModifiers();
  bool ctrlKeyIsDown = modifiers.testFlag(Qt::ControlModifier);

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
  if ((event->buttons() & Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
  }
}

void DrawWindow::mouseReleaseEvent(QMouseEvent *event)
{
  if ((event->button() & Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
    _dragging = false;
  }
}

void DrawWindow::changePenWidth()
{
  Q_ASSERT(_doodle != 0);
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
  Q_ASSERT(_doodle != 0);
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
  else
     QWidget::resizeEvent(event);
}

void DrawWindow::paintEvent(QPaintEvent *event)
{
  QPainter painter(this);
  painter.setRenderHint(QPainter::Antialiasing);
  // we just blit the from image to device
  QRect dirtyRect = event->rect();
  //qDebug() << "DrawWindow::paintEvent() - dirtyRect = " << dirtyRect;
  painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize& newSize, bool force/*=false*/)
{
  if (force || (_image.size() != newSize)) {
    qDebug() << "Resizing & repaining image as " << (force ? "forced" : "resized");
    QImage newImage(newSize, QImage::Format_RGB32);
    //newImage.fill(qRgb(255,255,255));
    newImage.fill(Chocolaf::ChocolafPalette::Window_Color);
    // draw existing image over new image
    QPainter painter(&newImage);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.drawImage(QPoint(0,0), _image);
    _image = newImage;
  }
}

//
// Action response functions
//
void DrawWindow::fileNew()
{
  if (canClose()) {
    _doodle->newDoodle();
    //_image.fill(qRgb(255,255,255));
    _image.fill(Chocolaf::ChocolafPalette::Window_Color);
    update();
  }
}

void DrawWindow::fileOpen()
{
  if (canClose()) {
     QString fileName = QFileDialog::getOpenFileName(
        this, tr("Open Qt Scribble File"), QCoreApplication::applicationDirPath(), ScribbleFiles);
     if (!fileName.isEmpty() && _doodle->load(fileName)) {
        //clearImage();
        //_image.fill(qRgb(255,255,255));
        _image.fill(Chocolaf::ChocolafPalette::Window_Color);
        QPainter painter(&_image);
        painter.setRenderHint(QPainter::Antialiasing);
        _doodle->draw(painter);
        update();
    }
  }
}

void DrawWindow::fileSave()
{
  Q_ASSERT(_doodle != 0);
  if (_doodle->isNew())
    fileSaveAs();
  else {
    _doodle->save(_doodle->filePath());
  }
}

void DrawWindow::fileSaveAs()
{
  QString fileName = QFileDialog::getSaveFileName(this, 
    tr("Save Qt Scribble File As"), _doodle->filePath(), ScribbleFiles);
  if (!fileName.isEmpty()) {
    _doodle->save(fileName);
  }
}





