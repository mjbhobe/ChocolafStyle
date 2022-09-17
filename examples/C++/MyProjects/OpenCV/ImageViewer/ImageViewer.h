#ifndef IMAGEVIEWER_H
#define IMAGEVIEWER_H

#include "ImageSpinner.h"
#include <QDir>
#include <QFileDialog>
#include <QMainWindow>
#include <QStringList>

class QLabel;
class QScrollArea;
class QScrollBar;
class QAction;
class QFileDialog;

QT_BEGIN_NAMESPACE
namespace Ui {
class ImageViewer;
}
QT_END_NAMESPACE

class ImageViewer : public QMainWindow
{
  Q_OBJECT

public:
  ImageViewer(QWidget *parent = nullptr);
  ~ImageViewer();

  bool loadImage(const QString &imagePath);
  void updateActions();
  void initializeFileDialog(QFileDialog &dialog, QFileDialog::AcceptMode acceptMode);

private slots:
  void open();
  void print();
  void zoomIn();
  void zoomOut();
  void rotateLeft();
  void rotateRight();
  void normalSize();
  void fitToWindow();
  void prevImage();
  void nextImage();
  void about();

private:
  void createActions();
  void createMenus();
  void createToolbar();
  void scaleImage(double factor = -1);
  void adjustScrollBar(QScrollBar *scrollBar, double factor);
  void setupStatusBar();
  void updateStatusBar();

  QImage *image;
  ImageSpinner *imageSpinner;
  bool imageLoaded;
  QLabel *imageLabel;
  QLabel *imageInfoLabel;
  QLabel *imageCountLabel;
  QLabel *scaleFactorLabel;
  QScrollArea *scrollArea;
  double scaleFactor;

  // actions
  QAction *openAction;
  QAction *printAction;
  QAction *exitAction;
  QAction *zoomInAction;
  QAction *zoomOutAction;
  QAction *zoomNormalAction;
  QAction *fitToWindowAction;
  QAction *rotateLeftAction;
  QAction *rotateRightAction;
  QAction *nextImageAction;
  QAction *prevImageAction;
  QAction *aboutAction;
  QAction *aboutQtAction;
};

#endif // IMAGEVIEWER_H
