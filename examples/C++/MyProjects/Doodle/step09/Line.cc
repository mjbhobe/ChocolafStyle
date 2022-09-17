// Line.cc: implements custom line class
#include "Line.h"
#include "MainWindow.h"
#include <QList>
#include <QtGui>

int adjustPenWidth(int penWidth)
{
   penWidth = qMin(qMax(1, penWidth), 12);
   return penWidth;
}

Line::Line(int penWidth /*= 2*/, const QColor &penColor /*= qRgb(0,0,255)*/)
{
   _penWidth = adjustPenWidth(penWidth);
   if (_penWidth <= 0) _penWidth = 2;
   _penColor = penColor;
   _points = new QList<QPoint>();
}

Line::~Line()
{
   delete _points;
}

void Line::setPenWidth(int newWidth)
{
   if (newWidth == _penWidth) return;

   _penWidth = adjustPenWidth(newWidth);
   qDebug() << "Line::setPenWidth() -> new pen width: " << _penWidth;
   emit penWidthChanged(_penWidth);
}

void Line::setPenColor(const QColor &newColor)
{
   if (_penColor == newColor) return;

   _penColor = newColor;
   emit penColorChanged(_penColor);
}

int Line::numPoints() const
{
   return (_points == nullptr) ? 0 : _points->count();
}

void Line::addPoint(const QPoint &pt)
{
   if (_points == nullptr) _points = new QList<QPoint>();
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

// -----------------------------------------------------
void Line::saveToStream(QDataStream &ds) const
{
   Q_ASSERT(_points != nullptr);

   // save pen width
   ds << qint32(_penWidth);
   qDebug() << QString("Line::saveToStream() - penWidth = %1").arg(_penWidth);
   /*
  int red, green, blue;
  red = _penColor.red();
  green = _penColor.green();
  blue = _penColor.blue();
  */
   // save pen color
   ds << qint32(_penColor.red()) << qint32(_penColor.green()) << qint32(_penColor.blue());
   qDebug() << QString("Line::saveToStream() - penColor = RGB(%1,%2,%3)")
                  .arg(_penColor.red())
                  .arg(_penColor.green())
                  .arg(_penColor.blue());
   // save the points themselves
   ds << _points->size();
   qDebug() << QString("Line::saveToStream() - saving %1 points").arg(_points->size());
   foreach (QPoint pt, *_points)
      ds << qint32(pt.x()) << qint32(pt.y());
}

void Line::loadFromStream(QDataStream &ds)
{
   qint32 penWidth;
   ds >> penWidth;
   _penWidth = penWidth;
   qDebug() << QString("Line::loadFromStream() - penWidth = %1").arg(_penWidth);

   qint32 red, green, blue;
   ds >> red >> green >> blue;
   _penColor = qRgb(red, green, blue);
   qDebug() << QString("Line::loadFromStream() - penColor = RGB(%1,%2,%3)")
                  .arg(_penColor.red())
                  .arg(_penColor.green())
                  .arg(_penColor.blue());

   qint32 numPoints;
   ds >> numPoints;
   qDebug() << QString("Line::loadFromStream() - expecting %1 points").arg(numPoints);
   QList<QPoint> *points = new QList<QPoint>();
   qint32 x, y;

   while (numPoints) {
      ds >> x >> y;
      points->append(QPoint(x, y));
      numPoints--;
   }
   delete _points;
   _points = points;
   qDebug() << QString("Line::loadFromStream() - loaded %1 points").arg(_points->size());
}

QDataStream &operator<<(QDataStream &ds, const Line &line)
{
   Q_ASSERT(line._points != nullptr);

   ds << qint32(line._penWidth);
   ds << line._penColor;
   ds << *(line._points);
   return ds;
}

QDataStream &operator>>(QDataStream &ds, Line &line)
{
   qint32 pw;
   ds >> pw;
   line._penWidth = pw;
   ds >> line._penColor;

   QList<QPoint> *points = new QList<QPoint>();
   ds >> (*points);
   // delete existing points & assign new
   if (line._points != nullptr) delete line._points;
   line._points = points;
   return ds;
}

QDataStream &operator<<(QDataStream &ds, const Line *line)
{
   Q_ASSERT(line != nullptr);
   ds << (*line);
   return ds;
}

QDataStream &operator>>(QDataStream &ds, Line *line)
{
   Q_ASSERT(line != nullptr);
   ds >> (*line);
   return ds;
}
