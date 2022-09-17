/****************************************************************************
**
** Copyright (C) 2016 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt Charts module of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:GPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 or (at your option) any later version
** approved by the KDE Free Qt Foundation. The licenses are as published by
** the Free Software Foundation and appearing in the file LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include <QtCharts/QAreaSeries>
#include <QtCharts/QChartView>
#include <QtCharts/QLineSeries>
#include <QtCore>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>

QT_CHARTS_USE_NAMESPACE

int main(int argc, char *argv[])
{
  QApplication app(argc, argv);

  // apply Chocolaf styling
  QFile f(":chocolaf/chocolaf.css");
  if (!f.exists()) {
    printf("Unable to open Chocolaf stylesheet! Using default LAF.");
  } else {
    f.open(QFile::ReadOnly | QFile::Text);
    QTextStream ts(&f);
    app.setStyleSheet(ts.readAll());
  }

  //![1]
  QLineSeries *series0 = new QLineSeries();
  QLineSeries *series1 = new QLineSeries();
  //![1]

  //![2]
  *series0 << QPointF(1, 5) << QPointF(3, 7) << QPointF(7, 6) << QPointF(9, 7)
           << QPointF(12, 6) << QPointF(16, 7) << QPointF(18, 5);
  *series1 << QPointF(1, 3) << QPointF(3, 4) << QPointF(7, 3) << QPointF(8, 2)
           << QPointF(12, 3) << QPointF(16, 4) << QPointF(18, 3);
  //![2]

  //![3]
  QAreaSeries *series = new QAreaSeries(series0, series1);
  series->setName("Batman");
  QPen pen(0x059605);
  pen.setWidth(3);
  series->setPen(pen);

  QLinearGradient gradient(QPointF(0, 0), QPointF(0, 1));
  gradient.setColorAt(0.0, 0x3cc63c);
  gradient.setColorAt(1.0, 0x26f626);
  gradient.setCoordinateMode(QGradient::ObjectBoundingMode);
  series->setBrush(gradient);
  //![3]

  //![4]
  QChart *chart = new QChart();
  chart->addSeries(series);
  chart->setTitle("<b>I am...Batman!</b>");
  chart->createDefaultAxes();
  chart->axes(Qt::Horizontal).first()->setRange(0, 20);
  chart->axes(Qt::Vertical).first()->setRange(0, 10);
  //![4]

  //![5]
  QChartView *chartView = new QChartView(chart);
  chartView->setRenderHint(QPainter::Antialiasing);
  //![5]

  //![6]
  QMainWindow window;
  window.setWindowTitle(QString("Qt %1 charts example").arg(QT_VERSION_STR));
  window.setCentralWidget(chartView);
  window.resize(640, 480);
  window.show();
  //![6]

  return app.exec();
}
