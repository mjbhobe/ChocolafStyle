#include "ImageViewer.h"
#include "ImageSpinner.h"
#include "common_funcs.h"
#include "ui_ImageViewer.h"
#include <QtCore>
#include <QtGui>
#include <QtWidgets>

class VLine : public QFrame
{
public:
  VLine(QWidget *parent = nullptr) : QFrame(parent)
  {
    setFrameShape(QFrame::VLine);
    setFrameShadow(QFrame::Sunken);
  }
};

ImageViewer::ImageViewer(QWidget *parent)
    : QMainWindow(parent), image(nullptr), imageSpinner(nullptr)
{
  setWindowTitle("ImageViewer");
  scaleFactor = 1.0;
  imageLoaded = false;
  imageLabel = new QLabel("");
  imageInfoLabel = new QLabel("");
  imageCountLabel = new QLabel("");
  scaleFactorLabel = new QLabel("");
  scrollArea = new QScrollArea();

  // imageLabel->setBackgroundRole(QPalette::Base);
  imageLabel->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
  imageLabel->setScaledContents(true);

  // scrollArea->setBackgroundRole(QPalette::Dark);
  scrollArea->setWidget(imageLabel);
  scrollArea->setVisible(false);
  setCentralWidget(scrollArea);

  createActions();
  createMenus();
  createToolbar();
  statusBar()->showMessage(
      QString("Qt %1 ImageViewer with Chocolaf theme").arg(QT_VERSION_STR));
  setupStatusBar();

  // set initial size to 3/5 of screen
  resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
  setWindowIcon(QIcon(":/app_icon.png")); // load an image
}

ImageViewer::~ImageViewer()
{
}

// helper function
QString getIconPath(QString baseName, bool darkTheme = false)
{
  QString iconPath =
      QString(":/%1_%2.png").arg(baseName).arg(darkTheme ? "dark" : "light");
  qDebug() << "Loading icon " << iconPath;
  return iconPath;
}

void ImageViewer::createActions()
{
  openAction = new QAction("&Open...", this);
  openAction->setShortcut(QKeySequence::Open);
  // openAction->setIcon(QIcon(":/open.png"));
  openAction->setIcon(QIcon(":/open.png"));
  openAction->setStatusTip("Open a new image file to view");
  QObject::connect(openAction, SIGNAL(triggered()), this, SLOT(open()));

  printAction = new QAction("&Print...", this);
  printAction->setShortcut(QKeySequence::Print);
  // printAction->setIcon(QIcon(":/print.png"));
  printAction->setIcon(QIcon(":/print.png"));
  printAction->setStatusTip("Print the current image");
  QObject::connect(printAction, SIGNAL(triggered()), this, SLOT(print()));
  printAction->setEnabled(false);

  exitAction = new QAction("E&xit", this);
  exitAction->setShortcut(QKeySequence("Ctrl+Q"));
  exitAction->setStatusTip("Quit the application");
  QObject::connect(exitAction, SIGNAL(triggered()), QApplication::instance(),
                   SLOT(quit()));

  zoomInAction = new QAction("Zoom &in (25%)", this);
  zoomInAction->setShortcut(QKeySequence("Ctrl++"));
  // zoomInAction->setIcon(QIcon(":/zoom_in.png"));
  zoomInAction->setIcon(QIcon(":/zoom_in.png"));
  zoomInAction->setStatusTip("Zoom into the image by 25%");
  QObject::connect(zoomInAction, SIGNAL(triggered()), this, SLOT(zoomIn()));
  zoomInAction->setEnabled(false);

  zoomOutAction = new QAction("Zoom &out (25%)", this);
  zoomOutAction->setShortcut(QKeySequence("Ctrl+-"));
  // zoomOutAction->setIcon(QIcon(":/zoom_out.png"));
  zoomOutAction->setIcon(QIcon(":/zoom_out.png"));
  zoomOutAction->setStatusTip("Zoom out of the image by 25%");
  QObject::connect(zoomOutAction, SIGNAL(triggered()), this, SLOT(zoomOut()));
  zoomOutAction->setEnabled(false);

  rotateLeftAction = new QAction("Rotate &left", this);
  rotateLeftAction->setShortcut(QKeySequence("Ctrl+<"));
  rotateLeftAction->setIcon(QIcon(":/rotate_left.png"));
  rotateLeftAction->setStatusTip("Rotate image counter-clockwise by 90 degrees");
  QObject::connect(rotateLeftAction, SIGNAL(triggered()), this, SLOT(rotateLeft()));
  rotateLeftAction->setEnabled(false);

  rotateRightAction = new QAction("Rotate &right", this);
  rotateRightAction->setShortcut(QKeySequence("Ctrl+>"));
  rotateRightAction->setIcon(QIcon(":/rotate_right.png"));
  rotateRightAction->setStatusTip("Rotate image clockwise by 90 degrees");
  QObject::connect(rotateRightAction, SIGNAL(triggered()), this, SLOT(rotateRight()));
  rotateRightAction->setEnabled(false);

  zoomNormalAction = new QAction("&Normal size", this);
  zoomNormalAction->setShortcut(QKeySequence("Ctrl+0"));
  zoomNormalAction->setStatusTip("Zoom to normal size (reset zoom)");
  QObject::connect(zoomNormalAction, SIGNAL(triggered()), this, SLOT(normalSize()));
  zoomNormalAction->setEnabled(false);

  fitToWindowAction = new QAction("Fit to &window", this);
  fitToWindowAction->setShortcut(QKeySequence("Ctrl+1"));
  // fitToWindowAction->setIcon(QIcon(":/fit_to_size.png"));
  fitToWindowAction->setIcon(QIcon(":/zoom_fit.png"));
  fitToWindowAction->setStatusTip("Fit the image to window");
  QObject::connect(fitToWindowAction, SIGNAL(triggered()), this, SLOT(fitToWindow()));
  fitToWindowAction->setEnabled(false);
  fitToWindowAction->setCheckable(true);

  prevImageAction = new QAction("&Previous image", this);
  prevImageAction->setShortcut(QKeySequence::MoveToPreviousChar); // left arrow (usually)
  // prevImageAction->setIcon(QIcon(":/previous.png"));
  prevImageAction->setIcon(QIcon(":/go_prev.png"));
  prevImageAction->setStatusTip("View previous image in folder");
  QObject::connect(prevImageAction, SIGNAL(triggered()), this, SLOT(prevImage()));
  prevImageAction->setEnabled(false);

  nextImageAction = new QAction("&Next image", this);
  nextImageAction->setShortcut(QKeySequence::MoveToNextChar); // right arrow (usually)
  // nextImageAction->setIcon(QIcon(":/next.png"));
  nextImageAction->setIcon(QIcon(":/go_next.png"));
  nextImageAction->setStatusTip("View next image in folder");
  QObject::connect(nextImageAction, SIGNAL(triggered()), this, SLOT(nextImage()));
  nextImageAction->setEnabled(false);

  aboutAction = new QAction("&About...", this);
  aboutAction->setStatusTip("Display the about information");
  QObject::connect(aboutAction, SIGNAL(triggered()), this, SLOT(about()));

  aboutQtAction = new QAction("About &Qt...", this);
  aboutQtAction->setStatusTip("Display information about the Qt library");
  QObject::connect(aboutQtAction, SIGNAL(triggered()), QApplication::instance(),
                   SLOT(aboutQt()));
}

void ImageViewer::createMenus()
{
  QMenu *fileMenu = menuBar()->addMenu("&File");
  fileMenu->addAction(openAction);
  fileMenu->addAction(printAction);
  fileMenu->addSeparator();
  fileMenu->addAction(exitAction);

  QMenu *viewMenu = menuBar()->addMenu("&View");
  viewMenu->addAction(zoomInAction);
  viewMenu->addAction(zoomOutAction);
  viewMenu->addAction(zoomNormalAction);
  viewMenu->addAction(fitToWindowAction);
  viewMenu->addSeparator();
  viewMenu->addAction(rotateLeftAction);
  viewMenu->addAction(rotateRightAction);
  viewMenu->addSeparator();
  viewMenu->addAction(prevImageAction);
  viewMenu->addAction(nextImageAction);

  QMenu *helpMenu = menuBar()->addMenu("Help");
  helpMenu->addAction(aboutAction);
  helpMenu->addAction(aboutQtAction);
}

void ImageViewer::createToolbar()
{
  QToolBar *toolBar = addToolBar("&Main");

  toolBar->addAction(openAction);
  toolBar->addAction(printAction);
  toolBar->addSeparator();
  toolBar->addAction(zoomInAction);
  toolBar->addAction(zoomOutAction);
  toolBar->addAction(fitToWindowAction);
  toolBar->addAction(rotateLeftAction);
  toolBar->addAction(rotateRightAction);
  toolBar->addSeparator();
  toolBar->addAction(prevImageAction);
  toolBar->addAction(nextImageAction);
}

void ImageViewer::updateActions()
{
  fitToWindowAction->setEnabled(imageLoaded);
  zoomInAction->setEnabled(!fitToWindowAction->isChecked());
  zoomOutAction->setEnabled(!fitToWindowAction->isChecked());
  zoomNormalAction->setEnabled(!fitToWindowAction->isChecked());
  prevImageAction->setEnabled(imageLoaded);
  nextImageAction->setEnabled(imageLoaded);
}

void ImageViewer::setupStatusBar()
{
  // statusBar()->reformat();
  statusBar()->setStyleSheet("QStatusBar::item {border: none;}");
  // statusBar()->addPermanentWidget(new VLine());
  statusBar()->addPermanentWidget(imageInfoLabel);
  statusBar()->addPermanentWidget(imageCountLabel);
  statusBar()->addPermanentWidget(scaleFactorLabel);
}

void ImageViewer::updateStatusBar()
{
  if (imageSpinner) {
#ifdef USING_QT6
    QImage image = imageLabel->pixmap().toImage();
#else
    QImage image = imageLabel->pixmap()->toImage();
#endif
    auto imageInfoText = QString("%1 x %2 %3")
                             .arg(image.width())
                             .arg(image.height())
                             .arg(image.isGrayscale() ? "grayscale" : "color");
    imageInfoLabel->setText(imageInfoText);
    auto sizeWidth = QString("%1").arg(imageSpinner->size()).length();
    QString status = QString("%1 of %2 images")
                         .arg(imageSpinner->currIndex() + 1, sizeWidth)
                         .arg(imageSpinner->size(), sizeWidth);
    qDebug() << status;
    imageCountLabel->setText(status);
    if (fitToWindowAction->isChecked()) {
      scaleFactorLabel->setText(QString("Zoom: %1").arg("Fit"));
    } else {
      auto currZoomFactor = int(scaleFactor * 100);
      scaleFactorLabel->setText(QString("Zoom: %1%").arg(currZoomFactor));
    }
  }
}

void ImageViewer::scaleImage(double factor /*= -1*/)
{
  // NOTE: factor == -1 is used to scale a newly loaded image to same
  // scaleFactor as last loaded image
  if (factor != -1)
    scaleFactor *= factor;
  imageLabel->resize(scaleFactor * imageLabel->pixmap(Qt::ReturnByValue).size());

  adjustScrollBar(scrollArea->horizontalScrollBar(), factor);
  adjustScrollBar(scrollArea->verticalScrollBar(), factor);

  zoomInAction->setEnabled(scaleFactor < 5.0);
  zoomOutAction->setEnabled(scaleFactor > 0.10);
}

void ImageViewer::adjustScrollBar(QScrollBar *scrollBar, double factor)
{
  scrollBar->setValue(
      int(factor * scrollBar->value() + ((factor - 1) * scrollBar->pageStep() / 2)));
}

bool ImageViewer::loadImage(const QString &imagePath)
{
  QImageReader reader(imagePath);
  reader.setAutoTransform(true);
  const QImage newImage = reader.read();
  if (newImage.isNull()) {
    imageLoaded = false;
    QMessageBox::information(this, "ImageViewer",
                             QString("FATAL: could not load image %1").arg(imagePath));
    return false;
  }

  // scaleFactor = 1.0;
  imageLoaded = true;
  scrollArea->setVisible(true);
  imageLabel->setPixmap(QPixmap::fromImage(newImage));
  imageLabel->adjustSize();
  scaleImage();

  QString title;
  QTextStream ostr(&title);
  ostr << "Qt " << QT_VERSION_STR << " ImageViewer: " << imagePath;
  setWindowTitle(title);

  // add ImageSpinner
  delete imageSpinner;
  imageSpinner = new ImageSpinner(imagePath);
  updateStatusBar();

  return true;
}

void ImageViewer::initializeFileDialog(QFileDialog &dialog,
                                       QFileDialog::AcceptMode acceptMode)
{
  const QStringList picsLocation =
      QStandardPaths::standardLocations(QStandardPaths::PicturesLocation);
  dialog.setDirectory(picsLocation.isEmpty() ? QDir::currentPath() : picsLocation.last());

  QStringList mimeTypeFilters;
  const QByteArrayList supportedMimeTypes = (acceptMode == QFileDialog::AcceptOpen)
                                                ? QImageReader::supportedMimeTypes()
                                                : QImageWriter::supportedMimeTypes();
  for (const QByteArray &mimeTypeName : supportedMimeTypes)
    mimeTypeFilters.append(mimeTypeName);
  mimeTypeFilters.sort();
  dialog.setMimeTypeFilters(mimeTypeFilters);
  dialog.selectMimeTypeFilter("image/jpeg");
  dialog.setAcceptMode(acceptMode);
  if (acceptMode == QFileDialog::AcceptSave)
    dialog.setDefaultSuffix("jpg");
}

void ImageViewer::open()
{
  QFileDialog dialog(this, "Open Image");
  initializeFileDialog(dialog, QFileDialog::AcceptOpen);

  if (dialog.exec() == QFileDialog::Accepted &&
      loadImage(dialog.selectedFiles().constFirst()))
    updateActions();
}

void ImageViewer::print()
{
  QMessageBox::information(this, "ImageViewer", "TODO: Implementation for Print Image");
}

void ImageViewer::zoomIn()
{
  scaleImage(1.25); // zoom in by 25%
  updateStatusBar();
}

void ImageViewer::zoomOut()
{
  scaleImage(0.75); // zoom out by 25%
  updateStatusBar();
}

void ImageViewer::normalSize()
{
  imageLabel->adjustSize();
  scaleFactor = 1.0;
  updateStatusBar();
}

void ImageViewer::fitToWindow()
{
  bool fitToWindow = fitToWindowAction->isChecked();
  scrollArea->setWidgetResizable(fitToWindow);
  if (!fitToWindow)
    normalSize();
  updateActions();
  updateStatusBar();
}

void ImageViewer::rotateLeft()
{
  // TODO
}

void ImageViewer::rotateRight()
{
  // TODO
}

void ImageViewer::prevImage()
{
  if (!imageSpinner->atFirst()) {
    QString imagePath = imageSpinner->prevImage();
    if (loadImage(imagePath))
      updateActions();
  } else {
    if (imageSpinner->atFirst())
      QMessageBox::information(this, "ImageViewer", "Displaying first image in folder!");
  }
}

void ImageViewer::nextImage()
{
  if (!imageSpinner->atLast()) {
    QString imagePath = imageSpinner->nextImage();
    if (loadImage(imagePath))
      updateActions();
  } else {
    if (imageSpinner->atLast())
      QMessageBox::information(this, "ImageViewer", "Displaying last image in folder!");
  }
}

void ImageViewer::about()
{
  QString str = QString("<b>Image Viewer</b> application to view images on desktop.<br/>"
                        "Created with Qt %1 and Chocolaf theme<br/><br/>"
                        "Developed by Manish Bhobe<br/>"
                        "Free to use, but use at your own risk!!")
                    .arg(QT_VERSION_STR);
  QMessageBox::about(this, tr("About Image Viewer"), str);
}
