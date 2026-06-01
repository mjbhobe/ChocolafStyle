#include <QBrush>
#include <QColor>
#include "PortfolioModel.h"

PortfolioModel::PortfolioModel(QObject *parent) : QAbstractTableModel(parent) {}

void PortfolioModel::populateData(const std::map<QString, int> &portfolio,
    const std::vector<QDate> &uniqueDates,
    const std::map<QString, std::vector<std::pair<QDate, double>>> &rawData)
{
  beginResetModel();
  m_columnsDates = uniqueDates;
  m_assets.clear();

  for (const auto &[ticker, shares]: portfolio) {
    TickerAsset asset;
    asset.symbol      = ticker;
    asset.sharesCount = shares;

    if (rawData.contains(ticker)) {
      for (const auto &[date, price]: rawData.at(ticker)) {
        asset.dateClosingPrices[date] = price;
      }
    }
    m_assets.push_back(asset);
  }
  endResetModel();
}

int PortfolioModel::rowCount(const QModelIndex &) const { return static_cast<int>(m_assets.size()); }
int PortfolioModel::columnCount(const QModelIndex &) const
{
  return 2 + static_cast<int>(m_columnsDates.size());
}

QVariant PortfolioModel::data(const QModelIndex &index, int role) const
{
  if (!index.isValid() || index.row() >= static_cast<int>(m_assets.size()))
    return QVariant();

  const auto &asset = m_assets[index.row()];

  // Visual Style Requirement: Shaded background color accent for the frozen columns
  if (role == Qt::BackgroundRole) {
    if (index.column() < 2) {
      return QBrush(QColor(230, 235, 240)); // Slightly darker slate-blue visual accent
    }
  }

  if (role == Qt::DisplayRole) {
    // Column 0: Ticker Code Symbol
    if (index.column() == 0)
      return asset.symbol;

    // Column 1: Total volume shares held
    if (index.column() == 1)
      return asset.sharesCount;

    // Columns 2+: Portfolio Value Calculation (Price * Number of Shares)
    int dateIndex    = index.column() - 2;
    QDate targetDate = m_columnsDates[dateIndex];

    if (asset.dateClosingPrices.contains(targetDate)) {
      double historicalPrice = asset.dateClosingPrices.at(targetDate);
      return historicalPrice * asset.sharesCount;
    }
    else {
      return "N/A"; // Handles non-trading days smoothly
    }
  }
  return QVariant();
}

QVariant PortfolioModel::headerData(int section, Qt::Orientation orientation, int role) const
{
  if (role != Qt::DisplayRole)
    return QVariant();

  if (orientation == Qt::Horizontal) {
    if (section == 0)
      return "Stock Symbol";
    if (section == 1)
      return "Shares Held";

    int dateIndex = section - 2;
    return m_columnsDates[dateIndex].toString("yyyy-MM-dd");
  }
  return QVariant();
}
