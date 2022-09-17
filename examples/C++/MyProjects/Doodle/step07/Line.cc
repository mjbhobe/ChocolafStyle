// Line.cc: implements custom line class
#include <QtGui>
#include <QList>
#include "Line.h"

Line::Line(int penWidth /*= 2*/, const QColor& penColor /*= qRgb(0,0,255)*/)
{
  _penWidth = penWidth;
  if (_penWidth <= 0) {
      _penWidth = 2;
      qDebug() << "WARNING: negative value specified for penWidth. "
        << "Reset to default value(=2)";
    }
  _penColor = penColor;
  _points = new QList<QPoint>();
}

Line::~Line()
{
  delete _points;
}

void Line::setPenWidth(int newWidth)
{
  if (newWidth == _penWidth)
    return;
  _penWidth = (newWidth <= 0) ? 2 : newWidth;
  qDebug() << "Line::setPenWidth() -> new pen width: " << _penWidth;
  emit penWidthChanged(_penWidth);
}

void Line::setPenColor(const QColor& newColor)
{
  if (_penColor == newColor)
    return;
  _penColor = newColor;
  emit penColorChanged(_penColor);
}

int Line::numPoints() const
{
  return (_points == 0) ? 0 : _points->count();
}

void Line::addPoint(const QPoint& pt)
{
  if (_points == 0)
    _points = new QList<QPoint>();
  _points->append(pt);
}

void Line::draw(QPainter& painter)
{
  qDebug() << "In Line::draw()...";

  if (numPoints() > 0) {
    QPen pen(_penColor, _penWidth);
    painter.setPen(pen);

    bool first = true;
    QPoint lastPt;

    foreach(QPoint pt, *_points) {
      if (!first)
        painter.drawLine(lastPt, pt);
      else
        first = false;
      lastPt = pt;
    }
  }
}
