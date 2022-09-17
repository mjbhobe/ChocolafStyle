// DrawWindow.cc: implements DrawWindow class
#include "DrawWindow.h"
#include "Doodle.h"
#include "Line.h"
#include "MainWindow.h"
#include "chocolaf.h"
#include <QApplication>
#include <QColorDialog>
#include <QDebug>
#include <QFileDialog>
#include <QInputDialog>
#include <QMessageBox>
#include <QtGui>

const QString ScribbleFiles("Qt Scribble Files (*.qscb)");

DrawWindow::DrawWindow()
{
  // setAttribute(Qt::WA_StaticContents);

  _dragging = false;
  _doodle = new Doodle();
  _currLine = nullptr;

  QObject::connect(_doodle, SIGNAL(doodleModified(bool)), this, SLOT(doodleModified(bool)));
  doodleModified(false);
}

void DrawWindow::doodleModified(bool modified)
{
  emit doodleModified2(modified);
}

DrawWindow::~DrawWindow()
{
  delete _doodle;
}

bool DrawWindow::canClose()
{
  if (_doodle->modified()) {
    switch (
      QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                            tr("The doodle has changed. Save changes to doodle now?"),
                            QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel,
                            QMessageBox::No)) {
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
  return true; // if not modified, I canClose()
}

void DrawWindow::closeEvent(QCloseEvent *event)
{
  if (canClose())
    event->accept();
  else
    event->ignore();
}

void DrawWindow::drawLineTo(const QPoint &pt)
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

void DrawWindow::clearImage(bool clearDoodle /*= true*/)
{
  Q_ASSERT(_doodle != nullptr);
  if (clearDoodle)
    _doodle->clear();
  // _image.fill(qRgb(255, 255, 255));
  _image.fill(Chocolaf::ChocolafPalette::Window_Color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  Q_ASSERT(_doodle != nullptr);

  // check if Ctrl key is held down as left/right mouse is clicked
  Qt::KeyboardModifiers modifiers = QApplication::queryKeyboardModifiers();
  bool ctrlKeyIsDown = modifiers.testFlag(Qt::ControlModifier);

  qDebug() << "mousePressEvent() - CTRL key " << (ctrlKeyIsDown ? "IS" : "IS **NOT**")
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

void DrawWindow::mouseMoveEvent(QMouseEvent *event)
{
  if ((event->buttons() == Qt::LeftButton) && _dragging) {
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
  int newPenWidth = QInputDialog::getInt(this, AppTitle, QString("Enter new pen width:"),
                                         _doodle->penWidth(), 2, 12, 1, &ok);
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
  qDebug() << "DrawWindow::resizeEvent() -> _image size(WxH) = (" << _image.width() << ","
           << _image.height() << ") client size (WxH) = (" << width() << "," << height()
           << ")";
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
   qDebug() << "DrawWindow::paintEvent() - dirtyRect = " << dirtyRect;
   painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize &newSize, bool force /*=false*/)
{
  if (force || (_image.size() != newSize)) {
    qDebug() << "Resizing & repaining image as " << (force ? "forced" : "resized");
    QImage newImage(newSize, QImage::Format_RGB32);
    //newImage.fill(qRgb(255,255,255));
    newImage.fill(Chocolaf::ChocolafPalette::Window_Color);
    // draw existing image over new image
    QPainter painter(&newImage);
    painter.setRenderHint(QPainter::Antialiasing);
    painter.drawImage(QPoint(0, 0), _image);
    _image = newImage;
    //update();
  }
}

//
// Action response functions
//
void DrawWindow::fileNew()
{
  if (canClose()) {
    _doodle->newDoodle();
    //clearImage(false);
    //_image.fill(qRgb(255, 255, 255));
    _image.fill(Chocolaf::ChocolafPalette::Window_Color);
    update();
  }
}

void DrawWindow::fileOpen()
{
  if (canClose()) {
    QString fileName = QFileDialog::getOpenFileName(this, tr("Open Qt Scribble File"),
                                                    QDir::currentPath(), ScribbleFiles);
    if (!fileName.isEmpty() && _doodle->load(fileName)) {
      //clearImage(false);
      //update();
      //_image.fill(qRgb(255,255,255));
      _image.fill(Chocolaf::ChocolafPalette::Window_Color);
      // clearImage(false);

      QPainter painter(&_image);
      painter.setRenderHint(QPainter::Antialiasing);
      _doodle->draw(painter);
      update();
    }
  }
}

void DrawWindow::fileSave()
{
  Q_ASSERT(_doodle != nullptr);
  if (_doodle->isNew())
    fileSaveAs();
  else {
    _doodle->save(_doodle->filePath());
  }
}

void DrawWindow::fileSaveAs()
{
  QString fileName = QFileDialog::getSaveFileName(this, tr("Save Qt Scribble File As"),
                                                  _doodle->filePath(), ScribbleFiles);
  if (!fileName.isEmpty()) {
    _doodle->save(fileName);
  }
}
