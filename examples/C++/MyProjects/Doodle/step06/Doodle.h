// Doodle.h - declares Doodle class (collection of Lines)
#ifndef __Doodle_h__
#define __Doodle_h__

#include <QtGui>
#include <QList>

class Line;

class Doodle  : public QObject {
    Q_OBJECT
  public:
    Doodle(int penWidth = 2, const QColor& penColor = qRgb(0,0,255));
    ~Doodle();

    Line* newLine();
    int numLines() const;
    int penWidth() const { return _penWidth; }
    void setPenWidth(int newWidth);
    QColor penColor() const { return _penColor; }
    void setPenColor(const QColor& color);
    void draw(QPainter& painter);
    bool modified() const { return _isModified; }
    void setModified(bool modified = true);
    void clear();
  private:
    QList<Line*> *_lines;
    int _penWidth;
    QColor _penColor;
    bool _isModified;
};

#endif  // __Doodle_h__
