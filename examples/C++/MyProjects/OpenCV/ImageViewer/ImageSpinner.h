#ifndef IMAGESPINNER_H
#define IMAGESPINNER_H

#include <QtCore>

class ImageSpinner : public QObject
{
public:
  ImageSpinner(const QString &imagePath);
  QString nextImage();
  QString prevImage();
  bool atFirst() const;
  bool atLast() const;
  qsizetype currIndex() const
  {
    return m_currIndex;
  }
  qsizetype size() const
  {
    return m_fileNames.size();
  }

protected:
  qsizetype m_currIndex;
  QDir m_dir;
  QStringList m_fileNames;
};

#endif // IMAGESPINNER_H
