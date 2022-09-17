#include "ImageSpinner.h"
#include "common_funcs.h"
#include "ui_ImageViewer.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

ImageSpinner::ImageSpinner(const QString &imagePath) : m_currIndex(-1)
{
  QFileInfo current(imagePath);
  m_dir = current.absoluteDir();
  QStringList imageFilters;
  imageFilters << "*.tiff"
               << "*.tif"
               << "*.jpg"
               << "*.jpeg"
               << "*.gif"
               << "*.bmp"
               << "*.png";
  m_fileNames = m_dir.entryList(imageFilters, QDir::Files, QDir::Name);
  // m_currIndex = m_fileNames.indexOf(QRegExp(QRegExp::escape(current.fileName())));
  m_currIndex = m_fileNames.indexOf(
      QRegularExpression(QRegularExpression::escape(current.fileName())));
}

QString ImageSpinner::prevImage()
{
  m_currIndex = m_currIndex - 1;
  if (m_currIndex < 0)
    m_currIndex = 0; // keep at 0th index
  QString prevImagePath =
      m_dir.absolutePath() + QDir::separator() + m_fileNames.at(m_currIndex);
  qDebug() << "Will display (prev): " << prevImagePath;
  // return dir.absoluteFilePath(m_fileNames.at(m_currIndex));
  return prevImagePath;
}

QString ImageSpinner::nextImage()
{
  m_currIndex = m_currIndex + 1;
  if (m_currIndex > m_fileNames.count() - 1)
    m_currIndex = m_fileNames.count() - 1; // keep at last index

  QString nextImagePath =
      m_dir.absolutePath() + QDir::separator() + m_fileNames.at(m_currIndex);
  qDebug() << "Will display (next): " << nextImagePath;
  // return dir.absoluteFilePath(m_fileNames.at(m_currIndex));
  return nextImagePath;
}

bool ImageSpinner::atFirst() const
{
  return m_currIndex == 0;
}

bool ImageSpinner::atLast() const
{
  return m_currIndex == m_fileNames.count() - 1;
}
