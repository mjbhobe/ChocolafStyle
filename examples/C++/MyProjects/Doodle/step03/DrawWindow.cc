// ============================================================================
// DrawWindow.cc: implements DrawWindow class, which handles the left & right
//   mouse clicks. Left mouse click shows the mouse position as (x, y) and
//   right mouse click clears all the left mouse click positions shown.
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include "DrawWindow.h"
#include "chocolaf.h"
#include <QGuiApplication>
#include <QMessageBox>
#include <QPalette>
#include <QtGlobal>
#include <QtGui>

DrawWindow::DrawWindow()
{
  setAttribute(Qt::WA_StaticContents);
  _modified = false;
}

void DrawWindow::drawPoint(const QPoint &pt)
{
  // display position where the mouse was clicked
  QString str;
  QTextStream ostr(&str); // like a string stream

  ostr << "(" << pt.x() << ", " << pt.y() << ")";

  QPainter painter(&_image);
  QFont font("Source Code Pro, Consolas, SF Mono, Monospace", 11);
  painter.setFont(font);
  // painter.setPen(getPaletteColor(QPalette::WindowText));
  // painter.setPen(Chocolaf::ChocolafPalette::WindowText_Color);
  painter.setPen(this->palette().color(QPalette::WindowText));
  painter.drawText(pt.x(), pt.y(), str);
  update();
}

void DrawWindow::clearImage()
{
  //_image.fill(qRgb(255, 255, 255));
  // QColor color = getPaletteColor(QPalette::Window);
  // QColor color = Chocolaf::ChocolafPalette::Window_Color;
  QColor color = this->palette().color(QPalette::Window);
  qDebug("clearImage() -> Color from palette %s", qPrintable(color.name()));
  _image.fill(color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  // if user clicks the left mouse button, then display position
  // where mouse was clicked. If right button pressed, clear the
  // entire drawing canvas
  if (event->button() == Qt::LeftButton) {
    drawPoint(QPoint(event->pos().x(), event->pos().y()));
    _modified = true;
    qDebug() << "DrawWindow::mousePressEvent() - _modified = True";
  }
  else if (event->button() == Qt::RightButton) {
    clearImage();
    _modified = false;
    qDebug() << "DrawWindow::mousePressEvent() - _modified = False";
  }
}

void DrawWindow::resizeEvent(QResizeEvent *event)
{
  if (width() > _image.width() || height() > _image.height()) {
    // need to expand image
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
  QString msg("Click the left mouse to show point & right mouse to clear");
  painter.drawText(10, 10, msg);
  QRect dirtyRect = event->rect();
  painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize &newSize)
{
  if (_image.size() == newSize)
    return;
  // create a  new image matching the new size
  QImage newImage(newSize, QImage::Format_RGB32);
  // QColor color = getPaletteColor(QPalette::Window);
  // QColor color = Chocolaf::ChocolafPalette::Window_Color;
  QColor color = this->palette().color(QPalette::Window);
  qDebug("resizeImage() -> Color from palette %s", qPrintable(color.name()));
  newImage.fill(color);

  // draw existing image over new image & mark it as new image
  QPainter painter(&newImage);
  painter.drawImage(QPoint(0, 0), _image);
  _image = newImage;
}

void DrawMainWindow::closeEvent(QCloseEvent *event)
{
  // window is about to close, prompt user & decide
  // if ok to quit based on user's response.
  qDebug() << "DrawMainWindow::closeEvent() called. _modified = "
           << (_drawWindow->isModified() ? "True" : "False");

  if (_drawWindow->isModified()) {
    switch (QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                                  tr("Contents of the doodle have changed.\nDo "
                                     "you want to quit without saving?"),
                                  QMessageBox::Yes | QMessageBox::No, QMessageBox::No))
    {
    case QMessageBox::Yes:
      // ok to quit
      qDebug() << "User chose to quit without saving...";
      event->accept();
      break;
    default:
      // don't quit yet
      event->ignore();
    }
  }
  else {
    event->accept();
  }
}
