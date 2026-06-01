#include <QDateTime>
#include <QLocale>
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include "DataFetcher.h"

using json = nlohmann::json;

DataFetcher::DataFetcher(QString ticker, QString startDateStr, QString endDateStr)
    : m_ticker(ticker), m_startDateStr(startDateStr), m_endDateStr(endDateStr)
{
}

qint64 DataFetcher::convertToUnixTimestamp(const QString &dateStr)
{
  QLocale englishLocale(QLocale::English, QLocale::UnitedStates);
  QDate date = englishLocale.toDate(dateStr, "dd-MMM-yyyy");
  if (!date.isValid())
    return -1;
  QDateTime dateTime(date, QTime(0, 0), Qt::UTC);
  return dateTime.toSecsSinceEpoch();
}

size_t DataFetcher::WriteCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  ((std::string *) userp)->append((char *) contents, size * nmemb);
  return size * nmemb;
}

std::vector<std::pair<QDate, double>> DataFetcher::fetchSynchronously()
{
  std::vector<std::pair<QDate, double>> extractedPoints;
  qint64 period1 = convertToUnixTimestamp(m_startDateStr);
  qint64 period2 = convertToUnixTimestamp(m_endDateStr);

  if (period1 == -1 || period2 == -1)
    return extractedPoints;

  CURL *curl = curl_easy_init();
  if (!curl)
    return extractedPoints;

  std::string url = "https://query1.finance.yahoo.com/v8/finance/chart/" + m_ticker.toStdString() +
      "?period1=" + std::to_string(period1) + "&period2=" + std::to_string(period2) + "&interval=1d";

  std::string readBuffer;
  curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
  curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
  curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
  curl_easy_setopt(curl, CURLOPT_USERAGENT, "Mozilla/5.0");

  CURLcode res = curl_easy_perform(curl);
  curl_easy_cleanup(curl);

  if (res != CURLE_OK)
    return extractedPoints;

  try {
    auto parsedJson = json::parse(readBuffer);
    if (!parsedJson.contains("chart") || parsedJson["chart"]["result"].is_null())
      return extractedPoints;

    auto &resultNode = parsedJson["chart"]["result"][0];
    if (!resultNode.contains("timestamp"))
      return extractedPoints;

    auto timestamps    = resultNode["timestamp"].get<std::vector<int64_t>>();
    auto closingPrices = resultNode["indicators"]["quote"][0]["close"].get<std::vector<json>>();

    for (size_t i = 0; i < timestamps.size(); ++i) {
      if (closingPrices[i].is_number()) {
        QDate date = QDateTime::fromSecsSinceEpoch(timestamps[i], Qt::UTC).date();
        extractedPoints.push_back({date, closingPrices[i].get<double>()});
      }
    }
  }
  catch (...) {
  }

  return extractedPoints;
}
