#include "StockModel.h"

StockModel::StockModel(QObject *parent) : QAbstractTableModel(parent) {}

int StockModel::rowCount(const QModelIndex &) const { return static_cast<int>(m_rows.size()); }
int StockModel::columnCount(const QModelIndex &) const { return 2; }

QVariant StockModel::data(const QModelIndex &index, int role) const
{
  if (!index.isValid() || index.row() >= static_cast<int>(m_rows.size()))
    return QVariant();

  if (role == Qt::DisplayRole) {
    const auto &row = m_rows[index.row()];
    if (index.column() == 0)
      return row.relianceClose > 0 ? QVariant(row.relianceClose) : QVariant("N/A");
    if (index.column() == 1)
      return row.itcClose > 0 ? QVariant(row.itcClose) : QVariant("N/A");
  }
  return QVariant();
}

QVariant StockModel::headerData(int section, Qt::Orientation orientation, int role) const
{
  if (role != Qt::DisplayRole)
    return QVariant();

  if (orientation == Qt::Horizontal) {
    if (section == 0)
      return "RELIANCE.NS (Close)";
    if (section == 1)
      return "ITC.NS (Close)";
  }
  else {
    if (section < static_cast<int>(m_rows.size())) {
      return m_rows[section].date.toString("yyyy-MM-dd");
    }
  }
  return QVariant();
}

void StockModel::updateData(const QString &ticker, const std::vector<std::pair<QDate, double>> &parsedData)
{
  beginResetModel();
  for (const auto &[date, close]: parsedData) {
    if (!m_dateToRowIndex.contains(date)) {
      StockRow newRow;
      newRow.date = date;
      m_rows.push_back(newRow);

      std::sort(
          m_rows.begin(), m_rows.end(), [](const StockRow &a, const StockRow &b) { return a.date < b.date; });

      m_dateToRowIndex.clear();
      for (size_t i = 0; i < m_rows.size(); ++i) {
        m_dateToRowIndex[m_rows[i].date] = static_cast<int>(i);
      }
    }

    int targetRow = m_dateToRowIndex[date];
    if (ticker == "RELIANCE.NS")
      m_rows[targetRow].relianceClose = close;
    else if (ticker == "ITC.NS")
      m_rows[targetRow].itcClose = close;
  }
  endResetModel();
}
