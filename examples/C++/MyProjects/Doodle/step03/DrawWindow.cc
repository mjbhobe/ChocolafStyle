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
#include <QtGlobal>
#include <QGuiApplication>
#include <QPalette>
#include <QMessageBox>
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
   //painter.setPen(getPaletteColor(QPalette::WindowText));
   painter.setPen(Chocolaf::ChocolafPalette::WindowText_Color);
   painter.drawText(pt.x(), pt.y(), str);
   update();
}

void DrawWindow::clearImage()
{
   //_image.fill(qRgb(255, 255, 255));
   //QColor color = getPaletteColor(QPalette::Window);
   QColor color = Chocolaf::ChocolafPalette::Window_Color;
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
   } else if (event->button() == Qt::RightButton) {
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
   QRect dirtyRect = event->rect();
   painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize &newSize)
{
   if (_image.size() == newSize)
      return;
   // create a  new image matching the new size
   QImage newImage(newSize, QImage::Format_RGB32);
   //QColor color = getPaletteColor(QPalette::Window);
   QColor color = Chocolaf::ChocolafPalette::Window_Color;
   qDebug("resizeImage() -> Color from palette %s", qPrintable(color.name()));
   newImage.fill(color);

   // draw existing image over new image & mark it as new image
   QPainter painter(&newImage);
   painter.drawImage(QPoint(0, 0), _image);
   _image = newImage;
}
