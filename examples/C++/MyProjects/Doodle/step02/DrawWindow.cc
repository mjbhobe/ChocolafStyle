// =============================================================================
// DrawWindow.cc: custom main window class.
//
// Tutorial - Qt Scribble Application - Step02
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobé for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include "DrawWindow.h"
#include <QMessageBox>
#include <QtGui>

DrawWidget::DrawWidget(QWidget *parent/*=nullptr*/)
  : QMainWindow(parent)
{
  // nothing more!
}

void DrawWidget::paintEvent(QPaintEvent *)
{
    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing);
    QString msg("This is the custom main window");
    // display a message asking user what to do
    painter.drawText(20, 20, msg);
}

