// ============================================================================
// main.cc: Creating a basic application with Qt/C++
//
// Tutorial - Qt Scribble Application - Step01
// Based on a similar tutorial for Borland ObjectWindows Library (OWL)
//
// @author Manish Bhobé for Nämostuté Ltd.
// My experiments with C++,Qt, Python & PyQt.
// Code is provided for illustration purposes only! Use at your own risk.
// =============================================================================
#include <QApplication>
#include <QMainWindow>
#include <QLocale>
#include <QLabel>
#include <format>

#include "chocolaf.h"

int main(int argc, char** argv)
{
  QApplication app(argc, argv);

  // show a label with currency conversion XXX USD = YYY INR @ 1 USD = RRR INR
  // where "XXX USD" displays a number formatted in USD currency notation
  // "YYY INR" displays the converted value in INR notation
  // assumes en_US and en_IN locales are installed on the OS and available to Qt.
  QLocale en_us{"en_US.utf-8"};
  QLocale en_in{"en_IN.utf-8"};
  constexpr auto curr{1225245.78};
  constexpr auto usd_to_inr{96.543};
  const auto label_str = QString::fromStdString(
    std::format(
      "{} is {} @ 1 USD = {} INR", en_us.toCurrencyString(curr).toStdString(),
      en_in.toCurrencyString(curr * usd_to_inr).toStdString(), usd_to_inr
    )
  );

  // create the GUI
  QMainWindow mainWindow;
  mainWindow.setWindowTitle(
    QString("Qt %1 Scribble - Step01: Basic Window").arg(QT_VERSION_STR)
  );
  mainWindow.resize(640, 480);
  QFont menuFont = QApplication::font();
  menuFont.setPointSize(14);
  mainWindow.setFont(menuFont);

  QLabel* label = new QLabel(label_str);
  label->setAlignment(Qt::AlignCenter | Qt::AlignVCenter);
  mainWindow.setCentralWidget(label);
  mainWindow.show();

  return app.exec();
}
