// Doodle.h - declares Doodle class (collection of Lines)
#ifndef __Doodle_h__
#define __Doodle_h__

#include <QtGui>
#include <QList>
#include <QDataStream>

class Line;

extern const QString DEF_FILE_NAME;
extern const QString DEF_FILE_EXT;
extern const QString OPEN_FILE_DESCR;
extern const QString AppTitle;
extern const QString WindowTitle;
extern const QColor DEF_PEN_COLOR;

class Doodle  : public QObject {
    Q_OBJECT
  public:
    Doodle(int penWidth = 2, const QColor& penColor = DEF_PEN_COLOR);
    ~Doodle();

    Line* newLine();
    int numLines() const;
    int penWidth() const { return _penWidth; }
    QColor penColor() const { return _penColor; }
    void draw(QPainter& painter);
    bool modified() const { return _isModified; }
    void clear();
    bool isNew() const { return _isNew; }
    QString filePath() const { return _filePath; }
    bool load(const QString& path);
    bool save(const QString& path);
    void newDoodle();

    // operators to save & load Doodle to DataStream
    friend QDataStream& operator << (QDataStream& ds, const Doodle& d);
    friend QDataStream& operator >> (QDataStream& ds, Doodle& d);
  public slots:
    void setPenWidth(int newWidth);
    void setPenColor(const QColor& color);
    void setNew(bool toNew = true);
    void setModified(bool modified = true);
  signals:
    void penWidthChanged(int /* newPenWidth*/);
    void penColorChanged(const QColor& /* newPenColor*/);
    void doodleIsNew(bool /* true_if_isNew_else_false */);
    void doodleModified(bool /* true_if_modified_else_false*/);
  private:
    // helper functions
    void clearLines(bool bInit = true);
    void saveToStream(QDataStream& ds) const;
    void loadFromStream(QDataStream& ds);

    QList<Line*> *_lines;
    int _penWidth, _defPenWidth;
    QColor _penColor, _defPenColor;
    bool _isModified;
    bool _isNew;
    QString _filePath;
};

#endif  // __Doodle_h__
