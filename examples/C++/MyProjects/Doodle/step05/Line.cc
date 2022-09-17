// Line.cc: implements custom line class
#include "Line.h"
#include <QList>
#include <QtGui>

Line::Line(int penWidth /*= 2*/, const QColor &penColor /*= qRgb(0,0,255)*/)
{
   // let's accept penwidths between 1 & 12 (inclusive) only
   penWidth = qMax(2, penWidth);
   penWidth = qMin(penWidth, 12);
   _penWidth = penWidth;
   _penColor = penColor;
   _points = new QList<QPoint>();
}

Line::~Line() { delete _points; }

void Line::setPenWidth(int newWidth)
{
   if (newWidth == _penWidth)
      return;

   newWidth = qMax(2, newWidth);
   newWidth = qMin(newWidth, 12);
   _penWidth = newWidth;
   qDebug() << "Line::setPenWidth() -> new pen width: " << _penWidth;
   emit penWidthChanged(_penWidth);
}

void Line::setPenColor(const QColor &newColor)
{
   if (_penColor == newColor)
      return;

   _penColor = newColor;
   emit penColorChanged(_penColor);
}

int Line::numPoints() const { return (_points == nullptr) ? 0 : _points->count(); }

void Line::addPoint(const QPoint &pt)
{
   if (_points == nullptr)
      _points = new QList<QPoint>();
   _points->append(pt);
}

void Line::draw(QPainter &painter)
{
   qDebug() << "In Line::draw()...";

   if (numPoints() > 0) {
      QPen pen(_penColor, _penWidth);
      painter.setPen(pen);

      bool first = true;
      QPoint lastPt;

      foreach (QPoint pt, *_points) {
         if (!first)
            painter.drawLine(lastPt, pt);
         else
            first = false;
         lastPt = pt;
      }
   }
}
