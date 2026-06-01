#include <CLI/CLI.hpp>
#include <QApplication>
#include <QDate>
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <curl/curl.h>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "DataFetcher.h"
#include "MainWindow.h"

// Struct to pass configuration down to the GUI
struct AppConfig {
    std::map<QString, int> portfolio;
    QString startDateStr;
    QString endDateStr;
    std::map<QString, std::vector<std::pair<QDate, double>>> downloadedData;
};

std::map<QString, int> readPortfolioCSV()
{
  std::map<QString, int> portfolio;
  QFile file("portfolio.csv");
  if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    std::cerr << "Error: Could not open portfolio.csv in execution directory.\n";
    return portfolio;
  }

  QTextStream in(&file);
  while (!in.atEnd()) {
    QString line = in.readLine().trimmed();
    if (line.isEmpty())
      continue;
    QStringList parts = line.split(',');
    if (parts.size() >= 2) {
      QString symbol    = parts[0].trimmed();
      int shares        = parts[1].trimmed().toInt();
      portfolio[symbol] = shares;
    }
  }
  return portfolio;
}

int main(int argc, char *argv[])
{
  curl_global_init(CURL_GLOBAL_DEFAULT);

  CLI::App cliApp{"Portfolio Value History Viewer"};

  std::string startOpt = "";
  std::string endOpt   = "";

  cliApp.add_option("--start", startOpt, "Start date in dd-MMM-yyyy format");
  cliApp.add_option("--end", endOpt, "End date in dd-MMM-yyyy format");

  try {
    cliApp.parse(argc, argv);
  }
  catch (const CLI::ParseError &e) {
    return cliApp.exit(e);
  }

  // 1. Process CLI Dates
  QLocale englishLocale(QLocale::English, QLocale::UnitedStates);
  QDate endDate;
  if (endOpt.empty()) {
    endDate = QDate::currentDate(); // today's date, if not specified
  }
  else {
    endDate = englishLocale.toDate(QString::fromStdString(endOpt), "dd-MMM-yyyy");
  }

  QDate startDate;
  if (startOpt.empty()) {
    // if not specified, then 30 days prev to end date
    startDate = endDate.addDays(-30);
  }
  else {
    startDate = englishLocale.toDate(QString::fromStdString(startOpt), "dd-MMM-yyyy");
  }

  if (!startDate.isValid() || !endDate.isValid() || startDate > endDate) {
    std::cerr << "Error: Invalid date range configurations evaluated.\n";
    return -1;
  }

  QString startDateStr = englishLocale.toString(startDate, "dd-MMM-yyyy");
  QString endDateStr   = englishLocale.toString(endDate, "dd-MMM-yyyy");

  // 2. Read Portfolio
  auto portfolio = readPortfolioCSV();
  if (portfolio.empty()) {
    std::cerr << "No assets parsed. Exiting application.\n";
    return -1;
  }

  // 3. Synchronous Console Downloads with interactive logging
  std::cout << "Downloading prices from start date (=" << startDateStr.toStdString()
            << ") to end date (=" << endDateStr.toStdString() << ") ...\n";

  std::map<QString, std::vector<std::pair<QDate, double>>> downloadedData;

  for (const auto &[ticker, shares]: portfolio) {
    std::cout << "  " << ticker.toStdString() << " - " << std::flush;

    // Run Fetcher synchronously for terminal output tracking requirement
    DataFetcher fetcher(ticker, startDateStr, endDateStr);
    auto data = fetcher.fetchSynchronously();

    if (data.empty()) {
      std::cout << "failed (check ticker or connectivity)\n";
    }
    else {
      std::cout << "ok\n";
      downloadedData[ticker] = data;
    }
  }

  // 4. Pass control over to Qt Graphical Architecture Frame
  QApplication app(argc, argv);

  MainWindow win;
  win.initializeData(portfolio, startDate, endDate, downloadedData);
  win.show();

  int execResult = app.exec();
  curl_global_cleanup();
  return execResult;
}
