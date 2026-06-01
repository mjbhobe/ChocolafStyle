#pragma once
#include <QAbstractTableModel>
#include <QDate>
#include <QString>
#include <map>
#include <vector>

struct TickerAsset {
    QString symbol;
    int sharesCount;
    std::map<QDate, double> dateClosingPrices;
};

class PortfolioModel : public QAbstractTableModel {
    Q_OBJECT
  public:
    explicit PortfolioModel(QObject *parent = nullptr);

    void populateData(const std::map<QString, int> &portfolio, const std::vector<QDate> &uniqueDates,
        const std::map<QString, std::vector<std::pair<QDate, double>>> &rawData);

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;
  private:
    std::vector<TickerAsset> m_assets;
    std::vector<QDate> m_columnsDates;
};
