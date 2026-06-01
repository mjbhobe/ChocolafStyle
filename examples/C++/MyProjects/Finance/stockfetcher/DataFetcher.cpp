#include <QDateTime>
#include <QDebug>
#include <QLocale>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include "DataFetcher.h"

using json = nlohmann::json;

DataFetcher::DataFetcher(QString ticker, QString startDateStr, QString endDateStr, QObject *parent)
    : QThread(parent), m_ticker(ticker), m_startDateStr(startDateStr), m_endDateStr(endDateStr)
{
}

// Helper function to convert "dd-Mmm-yyyy" to a raw Unix epoch timestamp
qint64 DataFetcher::convertToUnixTimestamp(const QString &dateStr)
{
  // Explicitly parse English month representations (e.g. "Apr", "May") safely regardless of system locale
  QLocale englishLocale(QLocale::English, QLocale::UnitedStates);
  QDate date = englishLocale.toDate(dateStr, "dd-MMM-yyyy");

  if (!date.isValid()) {
    return -1;
  }

  // Convert midnight of that day to UTC seconds epoch time
  QDateTime dateTime(date, QTime(0, 0), Qt::UTC);
  return dateTime.toSecsSinceEpoch();
}

size_t DataFetcher::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  ((std::string *) userp)->append((char *) contents, size * nmemb);
  return size * nmemb;
}

void DataFetcher::run()
{
  qint64 period1 = convertToUnixTimestamp(m_startDateStr);
  qint64 period2 = convertToUnixTimestamp(m_endDateStr);

  if (period1 == -1 || period2 == -1) {
    emit errorOccurred(QString("Invalid Date string formatting provided to fetcher: %1 / %2")
            .arg(m_startDateStr, m_endDateStr));
    return;
  }

  CURL *curl = curl_easy_init();
  if (!curl) {
    emit errorOccurred("Failed to initialize libcurl environment workspace");
    return;
  }

  // Dynamic REST string concatenation using your generated Epoch ranges
  std::string url = "https://query1.finance.yahoo.com/v8/finance/chart/" + m_ticker.toStdString() +
      "?period1=" + std::to_string(period1) + "&period2=" + std::to_string(period2) + "&interval=1d";

  std::string readBuffer;
  curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
  curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");

  CURLcode res = curl_easy_perform(curl);
  curl_easy_cleanup(curl);

  if (res != CURLE_OK) {
    emit errorOccurred(QString("Network request error: %1").arg(curl_easy_strerror(res)));
    return;
  }

  std::vector<std::pair<QDate, double>> extractedPoints;
  try {
    auto parsedJson = json::parse(readBuffer);

    if (!parsedJson.contains("chart") || parsedJson["chart"]["result"].is_null()) {
      emit errorOccurred(QString("No financial records found for ticker symbol %1 inside requested timeframe")
              .arg(m_ticker));
      return;
    }

    auto &resultNode   = parsedJson["chart"]["result"][0];
    auto timestamps    = resultNode["timestamp"].get<std::vector<int64_t>>();
    auto closingPrices = resultNode["indicators"]["quote"][0]["close"].get<std::vector<json>>();

    for (size_t i = 0; i < timestamps.size(); ++i) {
      if (closingPrices[i].is_number()) {
        QDate date        = QDateTime::fromSecsSinceEpoch(timestamps[i], Qt::UTC).date();
        double closePrice = closingPrices[i].get<double>();
        extractedPoints.push_back({date, closePrice});
      }
    }
    emit dataFetched(m_ticker, extractedPoints);
  }
  catch (const std::exception &e) {
    emit errorOccurred(QString("JSON engine fault parsing payload %1: %2").arg(m_ticker, e.what()));
  }
}
