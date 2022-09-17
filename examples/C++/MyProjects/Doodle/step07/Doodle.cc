// Doodle.cc: implements the Doodle class
#include <QtGui>
#include <QList>
#include "Line.h"
#include "Doodle.h"

Doodle::Doodle(int penWidth, const QColor& penColor)
{
  _lines = new QList<Line*>();
  // fix width between 1 & 12
  penWidth = qMax(1, penWidth);
  penWidth = qMin(12, penWidth);
  _penWidth = penWidth;
  _defPenWidth = _penWidth;
  _penColor = penColor;
  _defPenColor = _penColor;
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

void Doodle::setPenWidth(int newPenWidth)
{
  if (_penWidth == newPenWidth)
    return;
  newPenWidth = qMax(1, newPenWidth);
  newPenWidth = qMin(12, newPenWidth);
  _penWidth = newPenWidth;
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
  _penWidth = _defPenWidth;
  _penColor = _defPenColor;
  _isNew = true;
  _isModified = false;
}





