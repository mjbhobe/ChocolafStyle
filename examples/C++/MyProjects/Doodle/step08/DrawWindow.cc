// DrawWindow.cc: implements DrawWindow class
#include <QAction>
#include <QApplication>
#include <QColorDialog>
#include <QFileDialog>
#include <QIcon>
#include <QInputDialog>
#include <QMenu>
#include <QMenuBar>
#include <QMessageBox>
#include <QScreen>
#include <QStatusBar>
#include <QToolBar>
#include <QtGui>

#include "DrawWindow.h"
#include "Doodle.h"
#include "Line.h"
#include "QtAwesome.h"
#include "chocolaf.h"
#include "constants.h"
#include "IconFont.h"

DrawWindow::DrawWindow(QWidget *parent/*=nullptr*/)
  : QMainWindow(parent)
{
  setAttribute(Qt::WA_StaticContents);
  setWindowTitle(WindowTitle);
  setWindowIcon(QIcon(":/icons/appIcon.png"));

  createActions();
  createMenus();
  createToolbar();
  statusBar()->showMessage(
    QString("%1 - Doodling Application by %2. Created by Manish Bhobé").arg(
      QApplication::instance()->applicationName()
    ).arg(QApplication::instance()->organizationName())
  );

  _dragging = false;
  _doodle = new Doodle();
  _currLine = nullptr;
}

DrawWindow::~DrawWindow()
{
  delete _doodle;
}

void DrawWindow::createActions()
{
  /* moving from QtAwesome to using Materaial Icon fonts
  fa::QtAwesome* awesome = new fa::QtAwesome(this);
  awesome->initFontAwesome();


  QVariantMap options{};
  //    options.insert("color", QColor(qRgb(255, 255, 255)));
  //    options.insert("color-off", QColor(qRgb(200, 200, 200)));
  QColor color_active = this->palette().color(QPalette::Highlight);
  options.insert("color-active", color_active);
  */

  // get recommended icon dimension for screen DPI
  int iconDim = IconFont::getRecommendedToolbarIconSize(this).width();

  //auto file_new_icon = awesome->icon(fa::fa_regular, fa::fa_file, options);
  //fileNewAction = new QAction(file_new_icon, tr("&New"), this);
  fileNewAction = new QAction(tr("&New"), this);
  fileNewAction->setIcon(IconFont::getIcon(IconFont::Icons::FileNew, iconDim));
  fileNewAction->setShortcut(tr("Ctrl+N"));
  fileNewAction->setStatusTip(tr("Create a new scribble document."));
  QObject::connect(fileNewAction, SIGNAL(triggered()), this, SLOT(fileNew()));

  //auto file_open_icon = awesome->icon(fa::fa_regular, fa::fa_folder_open, options);
  //fileOpenAction = new QAction(file_open_icon, tr("&Open..."), this);
  fileOpenAction = new QAction(tr("&Open..."), this);
  fileOpenAction->setIcon(IconFont::getIcon(IconFont::Icons::FileOpen, iconDim));
  fileOpenAction->setShortcut(tr("Ctrl+O"));
  fileOpenAction->setStatusTip(tr("Open scribble document from disk file."));
  QObject::connect(fileOpenAction, SIGNAL(triggered()), this, SLOT(fileOpen()));

  //auto file_save_icon = awesome->icon(fa::fa_regular, fa::fa_save, options);
  //fileSaveAction = new QAction(file_save_icon, tr("&Save"), this);
  fileSaveAction = new QAction(tr("&Save"), this);
  fileSaveAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSave, iconDim));
  fileSaveAction->setShortcut(tr("Ctrl+S"));
  fileSaveAction->setStatusTip(tr("Save scribble document to disk file."));
  QObject::connect(fileSaveAction, SIGNAL(triggered()), this, SLOT(fileSave()));

  //auto file_saveas_icon = awesome->icon(fa::fa_regular, fa::fa_floppy_disk, options);
  //fileSaveAction = new QAction(file_saveas_icon, tr("&Save"), this);
  // auto file_saveas_icon = awesome->icon(fa::fa_regular,
  // fa::floppy_disk_pen, options);
  //fileSaveAsAction = new QAction(QIcon(":/icons/fileSaveAs.png"), tr("Save &as..."), this);
  fileSaveAsAction = new QAction(tr("Save &as..."), this);
  fileSaveAsAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSaveAs, iconDim));
  fileSaveAsAction->setStatusTip(tr("Save scribble document to disk with different name."));
  QObject::connect(fileSaveAsAction, SIGNAL(triggered()), this, SLOT(fileSaveAs()));

  exitAction = new QAction(tr("E&xit"), this);
  exitAction->setStatusTip(tr("Save all pending changes and quit application."));
  QObject::connect(exitAction, SIGNAL(triggered()), this, SLOT(close()));

  // auto pen_icon = awesome->icon(fa::fa_regular, fa::fa_pen, options);
  // penWidthAction = new QAction(pen_icon, tr("Change pen &width..."), this);
  //penWidthAction = new QAction(
  //  QIcon(":/icons/penWidth.png"), tr("Change pen &width..."), this
  //);
  penWidthAction = new QAction(tr("Change pen &width..."), this);
  penWidthAction->setIcon(IconFont::getIcon(IconFont::Icons::LineWeight, iconDim));
  penWidthAction->setStatusTip(tr("Change the width of default pen."));
  QObject::connect(penWidthAction, SIGNAL(triggered()), this, SLOT(changePenWidth()));

  //penColorAction = new QAction(
  //  QIcon(":/icons/penColor.png"), tr("Change pen &color..."), this
  //);
  penColorAction = new QAction(tr("Change pen &color..."), this);
  penColorAction->setIcon(IconFont::getIcon(IconFont::Icons::ColorLens, iconDim));
  penColorAction->setStatusTip(tr("Change the color of default pen."));
  QObject::connect(penColorAction, SIGNAL(triggered()), this, SLOT(changePenColor()));

  aboutQtAction = new QAction(tr("&About Qt..."), this);
  aboutQtAction->setStatusTip(tr("Display information about Qt library."));
  QObject::connect(aboutQtAction, SIGNAL(triggered()), qApp, SLOT(aboutQt()));

  aboutAction = new QAction(tr("&About..."), this);
  aboutAction->setStatusTip(tr("Display information about program."));
  QObject::connect(aboutAction, SIGNAL(triggered()), this, SLOT(about()));
}

void DrawWindow::createMenus()
{
  fileMenu = new QMenu(tr("&File"), this);
  fileMenu->addAction(fileNewAction);
  fileMenu->addAction(fileOpenAction);
  fileMenu->addAction(fileSaveAction);
  fileMenu->addAction(fileSaveAsAction);
  fileMenu->addSeparator();
  fileMenu->addAction(exitAction);

  optionsMenu = new QMenu(tr("&Options"), this);
  optionsMenu->addAction(penWidthAction);
  optionsMenu->addAction(penColorAction);

  helpMenu = new QMenu(tr("&Help"), this);
  helpMenu->addAction(aboutAction);
  helpMenu->addAction(aboutQtAction);

  menuBar()->addMenu(fileMenu);
  menuBar()->addMenu(optionsMenu);
  menuBar()->addMenu(helpMenu);
}

void DrawWindow::createToolbar()
{
  this->toolbar = new QToolBar();

  // Set the toolbar to display larger icons matching high-DPI scaling
  this->toolbar->setIconSize(IconFont::getRecommendedToolbarIconSize(this));

  this->toolbar->addAction(fileNewAction);
  this->toolbar->addAction(fileOpenAction);
  this->toolbar->addAction(fileSaveAction);
  this->toolbar->addAction(fileSaveAsAction);
  this->toolbar->addSeparator();
  this->toolbar->addAction(penWidthAction);
  this->toolbar->addAction(penColorAction);
  addToolBar(this->toolbar);
}

bool DrawWindow::canClose()
{
  if (_doodle->modified()) {
    switch (QMessageBox::question(
      this, tr("Qt Scribble Tutorial"),
      tr("The doodle has changed. Save changes to doodle now?"),
      QMessageBox::Yes | QMessageBox::No | QMessageBox::Cancel, QMessageBox::No
    )) {
      case QMessageBox::Yes:
        // save doodle & quit
        fileSave();
        return true;
      case QMessageBox::No:
        // quit without saving
        return true;
      default:
        // don't quit yet!
        return false;
    }
  }
  return true; // doodle not modified. Ok to quit!
}

void DrawWindow::updateActionIcons()
{
  int iconDim = IconFont::getRecommendedToolbarIconSize(this).width();

  if (fileNewAction)
    fileNewAction->setIcon(IconFont::getIcon(IconFont::Icons::FileNew, iconDim));
  if (fileOpenAction)
    fileOpenAction->setIcon(IconFont::getIcon(IconFont::Icons::FileOpen, iconDim));
  if (fileSaveAction)
    fileSaveAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSave, iconDim));
  if (fileSaveAsAction)
    fileSaveAsAction->setIcon(IconFont::getIcon(IconFont::Icons::FileSaveAs, iconDim));
  if (penColorAction)
    penColorAction->setIcon(IconFont::getIcon(IconFont::Icons::ColorLens, iconDim));
  if (penWidthAction)
    penWidthAction->setIcon(IconFont::getIcon(IconFont::Icons::LineWeight, iconDim));
}

void DrawWindow::changeEvent(QEvent *event) {
  if (event->type() == QEvent::PaletteChange) {
    // Automatically redraw icons in new color when user toggles dark/light theme
    updateActionIcons();
  }
  QMainWindow::changeEvent(event);
}

void DrawWindow::closeEvent(QCloseEvent* event)
{
  if (canClose())
    event->accept();
  else
    event->ignore();
}

void DrawWindow::drawLineTo(const QPoint& pt)
{
  Q_ASSERT(_currLine != nullptr);
  // draw line from _lastPt to pt
  QPainter painter(&_image);
  QPen pen(_currLine->penColor(), _currLine->penWidth());
  painter.setRenderHint(QPainter::Antialiasing);
  painter.setPen(pen);
  painter.drawLine(_lastPt, pt);
  _lastPt = pt;
  update();
}

void DrawWindow::clearImage()
{
  Q_ASSERT(_doodle != nullptr);
  _doodle->clear();

  //_image.fill(qRgb(255,255,255));
  _image.fill(Chocolaf::ChocolafPalette::Window_Color);
  update();
}

void DrawWindow::mousePressEvent(QMouseEvent* event)
{
  Q_ASSERT(_doodle != nullptr);

  // check if Ctrl key is held down as left/right mouse is clicked
  Qt::KeyboardModifiers modifiers = QApplication::queryKeyboardModifiers();
  bool ctrlKeyIsDown = modifiers.testFlag(Qt::ControlModifier);

  qDebug() << "mousePressEvent() - CTRL key " << (ctrlKeyIsDown ? "IS" : "IS **NOT**") <<
    " held down!";

  if (event->button() == Qt::LeftButton) {
    // left mouse button pressed
    if (ctrlKeyIsDown)
      changePenWidth();
    else {
      _currLine = _doodle->newLine();
      _lastPt = event->pos();
      _currLine->addPoint(_lastPt);
      _dragging = true;
      _doodle->setModified(true);
    }
  }
  else if (event->button() == Qt::RightButton) {
    if (ctrlKeyIsDown)
      changePenColor();
    else {
      clearImage();
      _doodle->setModified(false);
    }
  }
}

void DrawWindow::mouseMoveEvent(QMouseEvent* event)
{
  if ((event->buttons() == Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
  }
}

void DrawWindow::mouseReleaseEvent(QMouseEvent* event)
{
  if ((event->button() == Qt::LeftButton) && _dragging) {
    drawLineTo(event->pos());
    _currLine->addPoint(event->pos());
    _dragging = false;
  }
}

void DrawWindow::changePenWidth()
{
  Q_ASSERT(_doodle != nullptr);
  // display message box & get width of pen
  bool ok;
  int newPenWidth = QInputDialog::getInt(
    this, AppTitle, QString("Enter new pen width:"), _doodle->penWidth(), 2, 12, 1, &ok
  );
  if (ok) {
    qDebug() << "New pen width selected: " << newPenWidth;
    _doodle->setPenWidth(newPenWidth);
  }
}

void DrawWindow::changePenColor()
{
  Q_ASSERT(_doodle != nullptr);
  // display standard color dialog & get new pen color
  QColor color = QColorDialog::getColor(_doodle->penColor(), this);
  if (color.isValid())
    _doodle->setPenColor(color);
}

void DrawWindow::resizeEvent(QResizeEvent* event)
{
  if (width() > _image.width() || height() > _image.height()) {
    int newWidth = qMax(width(), _image.width());
    int newHeight = qMax(height(), _image.height());
    resizeImage(QSize(newWidth, newHeight));
    update();
  }
  QWidget::resizeEvent(event);
}

void DrawWindow::paintEvent(QPaintEvent* event)
{
  QPainter painter(this);
  painter.setRenderHint(QPainter::Antialiasing);
  // we just blit the from image to device
  QRect dirtyRect = event->rect();
  painter.drawImage(dirtyRect, _image, dirtyRect);
}

void DrawWindow::resizeImage(const QSize& newSize)
{
  if (_image.size() == newSize)
    return;
  QImage newImage(newSize, QImage::Format_RGB32);
  newImage.fill(qRgb(255, 255, 255));
  newImage.fill(Chocolaf::ChocolafPalette::Window_Color);

  // draw existing image over new image
  QPainter painter(&newImage);
  painter.setRenderHint(QPainter::Antialiasing);
  painter.drawImage(QPoint(0, 0), _image);
  _image = newImage;
}

//
// Action response functions
//
void DrawWindow::fileNew()
{
  if (canClose())
    clearImage();
}

void DrawWindow::fileOpen()
{
  QMessageBox::information(this, AppTitle, tr("File|Open clicked!"));
}

void DrawWindow::fileSave()
{
  Q_ASSERT(_doodle != 0);
  if (_doodle->isNew())
    fileSaveAs();
  else {
    // TODO:
  }
}

void DrawWindow::fileSaveAs()
{
  QString currFileName("");
  QString fileName = QFileDialog::getSaveFileName(this, tr("Save As"), currFileName);
  if (!fileName.isEmpty()) {
    QString str;
    QTextStream ostr(&str);
    ostr << tr("Will save file to: ") << fileName;
    QMessageBox::information(this, tr("File Save As..."), str);
  }
}

void DrawWindow::exitApp()
{
  QMessageBox::information(this, AppTitle, tr("File|Exit clicked!"));
}

void DrawWindow::about()
{
  /*
 QString str;
 QTextStream ostr(&str);
 ostr << "<html><b>Qt Scribble</b> - Doodling application<p/>Developed with the
 Qt "
      << QT_VERSION_STR << " C++ framework.<p/><p/>Written by - Manish
 Bhobé.<p/><p/>"
      << "<small>Program developed for illustration purposes only! Use at your
 own "
      << "risk! Author is not responsible for any damages (direct or indirect)
 that "
      << "may result from the use of this program.</small></html>"; */

  QString str = QString(
    "<html><b>Qt Scribble</b> - Doodling application<p/>Developed " "with the Qt "
    "%1 C++ framework.<p/><p/>Written by - %2.<p/>" "Copyright(C) %3<p/>"
    "<small>Program developed for illustration purposes only! Use at " "your own  "
    "risk! Author is not responsible for any damages (direct or " "indirect) that "
    "may result from the use of this program.</small></html>"
  ).arg(QT_VERSION_STR).arg(Chocolaf::__author__).arg(Chocolaf::__organization__);

  QMessageBox::about(this, AppTitle, str);
}
