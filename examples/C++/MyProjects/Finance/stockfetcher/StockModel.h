#pragma once
#include <QAbstractTableModel>
#include <QDate>
#include <QMap>
#include <QString>
#include <algorithm>
#include <vector>

struct StockRow {
    QDate date;
    double relianceClose = 0.0;
    double itcClose      = 0.0;
};

class StockModel : public QAbstractTableModel {
    Q_OBJECT
  public:
    explicit StockModel(QObject *parent = nullptr);

    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    int columnCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QVariant headerData(int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;

    void updateData(const QString &ticker, const std::vector<std::pair<QDate, double>> &parsedData);
  private:
    std::vector<StockRow> m_rows;
    QMap<QDate, int> m_dateToRowIndex;
};
