#pragma once
#include <QDate>
#include <QString>
#include <QThread>
#include <vector>

class DataFetcher : public QThread {
    Q_OBJECT
  signals:
    void dataFetched(QString ticker, std::vector<std::pair<QDate, double>> data);
    void errorOccurred(QString errorMsg);
  public:
    // Pass user-defined custom dates right into the constructor
    explicit DataFetcher(QString ticker, QString startDateStr, QString endDateStr, QObject *parent = nullptr);
    void run() override;
  private:
    QString m_ticker;
    QString m_startDateStr;
    QString m_endDateStr;

    qint64 convertToUnixTimestamp(const QString &dateStr);
    static size_t WriteCallback(void *contents, size_t size, size_t nmemb, void *userp);
};
