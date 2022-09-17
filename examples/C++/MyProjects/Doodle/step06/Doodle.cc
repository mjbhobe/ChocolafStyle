// ================================================================
// Doodle.cc: implements the Doodle class
//   doodle manages a collection of Line objects, each with it's
//   own thickness & color
// ================================================================
#include <QtGui>
#include <QList>
#include "Line.h"
#include "Doodle.h"

Doodle::Doodle(int penWidth, const QColor& penColor)
{
  _lines = new QList<Line*>();
  _penWidth = (penWidth <= 0) ? 2 : penWidth;
  _penColor = penColor;
  _isModified = false;
}

Doodle::~Doodle()
{
  if (_lines) {
    foreach(Line *line, *_lines)
      delete line;
  }
  delete _lines;
}

Line* Doodle::newLine()
{
  Line *line = new Line(_penWidth, _penColor);
  _lines->append(line);
  return line;
}

int Doodle::numLines() const
{
  return (_lines ? _lines->count() : 0);
}

void Doodle::setPenWidth(int newWidth)
{
  if (_penWidth == newWidth)
    return;

  newWidth = qMax(2, newWidth);
  newWidth = qMin(newWidth,12);
  _penWidth = newWidth;
}

void Doodle::setPenColor(const QColor& color)
{
  if (_penColor == color)
    return;
  _penColor = color;
}

void Doodle::draw(QPainter& painter)
{
  if (_lines) {
    QList<Line*>::iterator iter;
    for (iter = _lines->begin(); iter != _lines->end(); ++iter)
      (*iter)->draw(painter);
  }
}

void Doodle::setModified(bool modified)
{
  _isModified = modified;
}

void Doodle::clear()
{
  if (_lines) {
    foreach(Line *line, *_lines)
      delete line;
  }
  delete _lines;
  _lines = new QList<Line*>();
  _isModified = false;
}





