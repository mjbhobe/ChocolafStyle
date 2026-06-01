#pragma once
#include <QDate>
#include <QString>
#include <vector>

class DataFetcher {
  public:
    explicit DataFetcher(QString ticker, QString startDateStr, QString endDateStr);
    std::vector<std::pair<QDate, double>> fetchSynchronously();
  private:
    QString m_ticker;
    QString m_startDateStr;
    QString m_endDateStr;

    qint64 convertToUnixTimestamp(const QString &dateStr);
    static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp);
};
