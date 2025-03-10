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

#include "chocolaf.h"
#include <QtCharts/QBarCategoryAxis>
#include <QtCharts/QBarSeries>
#include <QtCharts/QBarSet>
#include <QtCharts/QChartView>
#include <QtCharts/QLegend>
#include <QtCharts/QValueAxis>
#include <QtCore>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>

// QT_CHARTS_USE_NAMESPACE

int main(int argc, char* argv[])
{
    //  Chocolaf::ChocolafApp::setupForHighDpiScreens();
    //  Chocolaf::ChocolafApp app(argc, argv);
    QApplication app(argc, argv);
    app.setStyle("Fusion");

    /*
    QApplication app(argc, argv);

    // apply Chocolaf styling
    QFile f(":chocolaf/chocolaf.css");
    if (!f.exists()) {
      printf("Unable to open stylesheet!");
    }
    else {
      f.open(QFile::ReadOnly | QFile::Text);
      QTextStream ts(&f);
      app.setStyleSheet(ts.readAll());
    }*/

    //![1]
    QBarSet* set0 = new QBarSet("Jane");
    QBarSet* set1 = new QBarSet("John");
    QBarSet* set2 = new QBarSet("Axel");
    QBarSet* set3 = new QBarSet("Mary");
    QBarSet* set4 = new QBarSet("Samantha");

    *set0 << 1 << 2 << 3 << 4 << 5 << 6;
    *set1 << 5 << 0 << 0 << 4 << 0 << 7;
    *set2 << 3 << 5 << 8 << 13 << 8 << 5;
    *set3 << 5 << 6 << 7 << 3 << 4 << 5;
    *set4 << 9 << 7 << 5 << 3 << 1 << 2;
    //![1]

    //![2]
    QBarSeries* series = new QBarSeries();
    series->append(set0);
    series->append(set1);
    series->append(set2);
    series->append(set3);
    series->append(set4);

    //![2]

    //![3]
    QChart* chart = new QChart();
    chart->addSeries(series);
    chart->setTitle("Simple barchart example");
    chart->setAnimationOptions(QChart::SeriesAnimations);
    //![3]

    //![4]
    QStringList categories;
    categories << "Jan"
               << "Feb"
               << "Mar"
               << "Apr"
               << "May"
               << "Jun";
    QBarCategoryAxis* axisX = new QBarCategoryAxis();
    axisX->append(categories);
    chart->addAxis(axisX, Qt::AlignBottom);
    series->attachAxis(axisX);

    QValueAxis* axisY = new QValueAxis();
    axisY->setRange(0, 15);
    chart->addAxis(axisY, Qt::AlignLeft);
    series->attachAxis(axisY);
    //![4]

    //![5]
    chart->legend()->setVisible(true);
    chart->legend()->setAlignment(Qt::AlignBottom);
    //![5]

    //![6]
    QChartView* chartView = new QChartView(chart);
    chartView->setRenderHint(QPainter::Antialiasing);
    //![6]

    //![7]
    QMainWindow window;
    window.setCentralWidget(chartView);
    // window.resize(1024, 768);
    Chocolaf::centerOnScreenWithSize(window, 0.75, 0.5);
    window.setWindowTitle(QString("Qt %1 barchart demo").arg(QT_VERSION_STR));
    window.show();
    //![7]

    return app.exec();
}
