// Doodle.cc: implements the Doodle class
#include <QtGui>
#include <QList>
#include <QFile>
#include <QMessageBox>
#include "Line.h"
#include "Doodle.h"

const QString DEF_FILE_NAME("untitled.qscb");
const QString DEF_FILE_EXT("qscb");
const QString OPEN_FILE_DESCR("Qt Scribble Files (*.qscb)");
const QColor DEF_PEN_COLOR = qRgb(0,64,128);

Doodle::Doodle(int penWidth /*= 2*/, const QColor& penColor /*= qRgb(0,0,255)*/)
{
  _lines = nullptr;
  _defPenWidth = penWidth;
  _defPenColor = penColor;
  newDoodle();
}

Doodle::~Doodle()
{
  clearLines(false);
}

void Doodle::clearLines(bool bInit /*= true*/)
{
  if (_lines) {
    foreach(Line *line, *_lines)
      delete line;
  }
  delete _lines;
  _lines = nullptr;
  if (bInit) _lines = new QList<Line*>();
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
  _penWidth = (newPenWidth <= 0) ? 2 : newPenWidth;
  emit penWidthChanged(_penWidth);
}

void Doodle::setPenColor(const QColor& color)
{
  if (_penColor == color)
    return;
  _penColor = color;
  emit penColorChanged(_penColor);
}

void Doodle::draw(QPainter& painter)
{
  if (_lines) {
    qDebug() << "Doodle::draw() - drawing " << _lines->size() << " lines";
    foreach(Line *line, *_lines) {
      qDebug() << QString("Doodle::draw() - drawing line with %1 points, penWidth = %2 and penColor = RGB(%3,%4,%5)")
        .arg(line->numPoints())
        .arg(line->penWidth())
        .arg(line->penColor().red())
        .arg(line->penColor().green())
        .arg(line->penColor().blue());
      line->draw(painter);
    }
  } else {
    qDebug() << "Doodle::draw() - NO lines to draw!";
  }
}

void Doodle::setNew(bool toNew)
{
  if (_isNew == toNew)
    return;
  _isNew = toNew;
  if (_isNew) _filePath = DEF_FILE_NAME;
  emit doodleIsNew(_isNew);
}

void Doodle::setModified(bool modified)
{
  if (_isModified == modified)
    return;
  _isModified = modified;
  emit doodleModified(_isModified);
}

void Doodle::newDoodle()
{
  clearLines();
  _penWidth = _defPenWidth;
  _penColor = _defPenColor;
  setNew(true);
  setModified(false);
}

void Doodle::clear()
{
  clearLines();
  setModified(true);
}

bool Doodle::load(const QString& path)
{
  // TODO: exception enable this function
  if (QFile::exists(path)) {
    QFile file(path);
    file.open(QIODevice::ReadOnly);
    QDataStream ds(&file);
    loadFromStream(ds);
    _filePath = path;
    setNew(false);
    setModified(false);
    qDebug() << "Doodle loaded successfully!";
    return true;
  }
  else {
    QString str;
    QTextStream ostr(&str);
    ostr << "FATAL ERROR: Doodle::load() -> file path is not valid (" << path << ")";
    QMessageBox::critical(nullptr, AppTitle, str);
    return false;
  }
}

bool Doodle::save(const QString& path)
{
  // TODO: exception enable this function
  QFile file(path);
  file.open(QIODevice::WriteOnly);
  QDataStream ds(&file);
  saveToStream(ds);
  setNew(false);
  _filePath = path;
  setModified(false);
  return true;
}

// -----------------------------------------------------
void Doodle::saveToStream(QDataStream& ds) const
{
  Q_ASSERT(_lines != nullptr);

  ds << qint32(_penWidth) << qint32(_defPenWidth);
  qDebug() << QString("Doodle::saveToStream() - saving penWidth = %1, defPenWidth = %2")
    .arg(_penWidth).arg(_defPenWidth);
  ds << qint32(_penColor.red()) << qint32(_penColor.green())
    << qint32(_penColor.blue());
  qDebug() << QString("Doodle::saveToStream() - saving penColor = RGB(%1,%2,%3)")
    .arg(_penColor.red()).arg(_penColor.green()).arg(_penColor.blue());
  ds << qint32(_defPenColor.red()) << qint32(_defPenColor.green())
    << qint32(_defPenColor.blue());
  qDebug() << QString("Doodle::saveToStream() - saving defPenColor = RGB(%1,%2,%3)")
    .arg(_defPenColor.red()).arg(_defPenColor.green()).arg(_defPenColor.blue());
  // save points
  ds << _lines->size();
  qDebug() << QString("Doodle::saveToStream() - saving %1 lines")
    .arg(_lines->size());
  foreach(Line *line, *_lines)
    line->saveToStream(ds);
}

void Doodle::loadFromStream(QDataStream& ds)
{
  qDebug() << "Doodle::loadFromStream()...";

  qint32 penWidth;
  ds >> penWidth;
  _penWidth = penWidth;
  ds >> penWidth;
  _defPenWidth = penWidth;
  qDebug() << QString("Doodle penWidth = %1, defPenWidth = %2")
    .arg(_penWidth).arg(_defPenWidth);

  qint32 red, green, blue;
  ds >> red >> green >> blue;
  qDebug() << QString("Doodle penColor = RGB(%1,%2,%3)")
    .arg(red).arg(green).arg(blue);
  _penColor = qRgb(red, green, blue);
  ds >> red >> green >> blue;
  qDebug() << QString("Doodle default penColor = RGB(%1,%2,%3)")
    .arg(red).arg(green).arg(blue);
  _defPenColor = qRgb(red, green, blue);

  qint32 numLines;
  ds >> numLines;
  qDebug() << QString("Number of lines = %1").arg(numLines);
  QList<Line*> *lines = new QList<Line*>();

  while(numLines) {
    Line *line = new Line;
    line->loadFromStream(ds);
    lines->append(line);
    numLines--;
  }
  foreach(Line *aLine, *_lines)
    delete aLine;
  delete _lines;
  _lines = lines;
  qDebug() << QString("Now _lines has %1 lines").arg(_lines->size());
}


QDataStream& operator << (QDataStream& ds, const Doodle& doodle)
{
  doodle.saveToStream(ds);
  return ds;
}

QDataStream& operator >> (QDataStream& ds, Doodle& doodle)
{
  doodle.loadFromStream(ds);
  return ds;
}



