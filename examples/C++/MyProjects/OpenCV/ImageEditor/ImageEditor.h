#ifndef IMAGEEDITOR_H
#define IMAGEEDITOR_H

#include <QDir>
#include <QFileDialog>
#include <QMainWindow>
#include <QStringList>

class QLabel;
class QScrollArea;
class QScrollBar;
class QAction;
class QFileDialog;
class QPixmap;
class ImageSpinner;

QT_BEGIN_NAMESPACE
namespace Ui {
class ImageEditor;
}
QT_END_NAMESPACE

class ImageEditor : public QMainWindow
{
  Q_OBJECT

public:
  ImageEditor(QWidget *parent = nullptr);
  ~ImageEditor();

  bool loadImage(const QString &imagePath);
  void initializeFileDialog(QFileDialog &dialog, QFileDialog::AcceptMode acceptMode);

  // save & restore state
  void writeSettings();
  void readSettings();

private slots:
  void open();
  void print();

  void blurImage();
  void sharpenImage();
  void erodeImage();
  void cartoonifyImage();

  void zoomIn();
  void zoomOut();
  void normalSize();
  void fitToWindow();
  void prevImage();
  void nextImage();

  void about();

private:
  void createActions();
  void createMenus();
  void createToolbar();
  void updateActions();
  void scaleImage(double factor = -1);
  void adjustScrollBar(QScrollBar *scrollBar, double factor);
  void setupStatusBar();
  void updateStatusBar();

  // QPixmap *m_pixmap;
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
  QAction *blurAction;
  QAction *sharpenAction;
  QAction *erodeAction;
  QAction *cartoonAction;
  QAction *exitAction;
  QAction *zoomInAction;
  QAction *zoomOutAction;
  // QAction *zoomNormalAction;
  QAction *fitToWindowAction;
  QAction *nextImageAction;
  QAction *prevImageAction;
  QAction *aboutAction;
  QAction *aboutQtAction;
};

#endif // IMAGEEDITOR_H
