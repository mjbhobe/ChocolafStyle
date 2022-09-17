// =============================================================================
// DrawWindow.cc: implements DrawWindow class, which handles left & right
//   mouse clicks + the window close event
//
// Tutorial - Qt Scribble Application
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobe for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include "DrawWindow.h"
#include <QMessageBox>
#include <QtGui>

DrawWindow::DrawWindow()
{
  QString title =
      QString("Qt %1 Doodle with Chocolaf - Step02: Handling Events").arg(QT_VERSION_STR);
  setWindowTitle(title);
  resize(QGuiApplication::primaryScreen()->availableSize() * 4 / 5);
}

void DrawWindow::closeEvent(QCloseEvent *event)
{
  // window is about to close, prompt user & decide if ok to quit or not
  // based on user's response.
  qDebug() << "DrawWindow::closeEvent() called!" << Qt::endl;
  auto ret =
      QMessageBox::question(this, tr("Qt Scribble Tutorial"),
                            tr("This will close the application.\nOk to quit now?"),
                            QMessageBox::Yes | QMessageBox::No, QMessageBox::No);

  switch (ret) {
    case QMessageBox::Yes:
      // ok to quit
      event->accept();
      break;
    default:
      // don't quit yet
      event->ignore();
  }
}

void DrawWindow::mousePressEvent(QMouseEvent *event)
{
  if (event->button() == Qt::LeftButton) {
    QMessageBox::information(this, tr("Qt Scribble Tutorial"),
                             tr("You have pressed the LEFT mouse button!"));
  } else if (event->button() == Qt::RightButton) {
    QMessageBox::information(this, tr("Qt Scribble Tutorial"),
                             tr("You have pressed the RIGHT mouse button!"));
  }
}
