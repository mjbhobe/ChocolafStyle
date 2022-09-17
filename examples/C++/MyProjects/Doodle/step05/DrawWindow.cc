// DrawWindow.cc: implements DrawWindow class
#include "chocolaf.h"
#include "DrawWindow.h"
#include "Line.h"
#include <QApplication>
#include <QColorDialog>
#include <QInputDialog>
#include <QMessageBox>
#include <QtGui>

const QString AppTitle("Qt Scribble");
const QString WindowTitle = QString("Qt %1 Doodle - Step05: Changing Line color & thickness").arg(QT_VERSION_STR);

DrawWindow::DrawWindow()
{
   setAttribute(Qt::WA_StaticContents);
   setWindowTitle(WindowTitle);
   _modified = false;
   _dragging = false;
   _penWidth = 3;
   _penColor = qRgb(0, 0, 255);
   _line = nullptr;
}

DrawWindow::~DrawWindow() { delete _line; }

void DrawWindow::closeEvent(QCloseEvent *event)
{
   // window is about to close, prompt user & decide if ok to quit
   // based on user's response.
   if (_modified) {
      switch (QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                                    tr("The doodle has been modified.\nDo you want to close without saving?"),
                                    QMessageBox::Yes | QMessageBox::No, QMessageBox::No)) {
         case QMessageBox::Yes:
            // ok to quit
            qDebug() << "User chose to quit without saving!";
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
   QPen pen(_penColor, _penWidth);
   painter.setRenderHint(QPainter::Antialiasing);
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
      if (QApplication::keyboardModifiers() & Qt::ControlModifier) {
         // display message box & get new width of pen
         // NOTE: this is not the best way to call up a dialog!!! It'll do for now
         bool ok;
         int newPenWidth = QInputDialog::getInt(this, AppTitle, QString("Enter new pen width (2-12):"),
                                                _line->penWidth(), 2, 12, 1, &ok);
         if (ok) {
            qDebug() << "New pen width selected: " << newPenWidth;
            _penWidth = newPenWidth;
         }
      } else {
         delete _line;
         _line = nullptr;
         clearImage();
         _lastPt = event->pos();
         _dragging = true;
         _modified = true;
         _line = new Line(_penWidth, _penColor);
         _line->addPoint(event->pos());
      }
   } else if (event->button() == Qt::RightButton) {
      if (QApplication::keyboardModifiers() & Qt::ControlModifier) {
         // if Ctrl key is also pressed, display standard color
         // dialog & get new pen color
         QColor color = QColorDialog::getColor(_penColor, this);
         if (color.isValid())
            _penColor = color;

      } else {
         clearImage();
         _modified = false;
      }
   }
}

void DrawWindow::mouseMoveEvent(QMouseEvent *event)
{
   if (event->buttons() & Qt::LeftButton && _dragging) {
      drawLineTo(event->pos());
      _line->addPoint(event->pos());
   }
}

void DrawWindow::mouseReleaseEvent(QMouseEvent *event)
{
   if ((event->button() == Qt::LeftButton) && _dragging) {
      drawLineTo(event->pos());
      _line->addPoint(event->pos());
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
   painter.setRenderHint(QPainter::Antialiasing);
   QRect dirtyRect = event->rect();
   painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize &newSize)
{
   if (_image.size() == newSize)
      return;
   QImage newImage(newSize, QImage::Format_RGB32);
   //newImage.fill(qRgb(255, 255, 255));
   newImage.fill(Chocolaf::ChocolafPalette::Window_Color);

   // draw existing image over new image
   QPainter painter(&newImage);
   painter.setRenderHint(QPainter::Antialiasing);
   painter.drawImage(QPoint(0, 0), _image);
   _image = newImage;
}
