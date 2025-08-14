// SysmetsModel.cpp - QAbstractTable model for system metrics
#include "SysmetsModel.h"
#include <windows.h>
#include "sysmets.h"

SysmetsModel::SysmetsModel(QObject *parent /*= null_ptr*/)
  : QAbstractTableModel(parent)
{
  // nothing more
}

int SysmetsModel::rowCount(const QModelIndex & /*parent*/) const
{
  return NUMLINES;
}

int SysmetsModel::columnCount(const QModelIndex & /*parent*/) const
{
  return 3; /* hard coded! */
}

QVariant SysmetsModel::headerData(
  int section, Qt::Orientation orientation, int role /*= Qt::DisplayRole*/) const
{
  if (role == Qt::DisplayRole && orientation == Qt::Horizontal) {
    switch (section) {
      case 0:
        return "Metric";
      case 1:
        return "Description";
      case 2:
        return "Value";
      default:
        return QVariant();
    }
  }
  return QVariant();
}

QVariant SysmetsModel::data(const QModelIndex &index, int role) const
{
  int row = index.row();
  int col = index.column();
  auto sysmets_row = sysmetrics[row];

  if (role == Qt::DisplayRole) {
    switch (index.column()) {
      case 0: {
        // first col shows label
        return sysmets_row.szLabel;
      } break;
      case 1: {
        // 2nd col shows description of metric
        return sysmets_row.szDesc;
      } break;
      case 2: {
        // 3rd col shows value
        return QString("%1").arg(::GetSystemMetrics(sysmets_row.iIndex));
      } break;
      default:
        break;
    }
  } else if (role == Qt::TextAlignmentRole) {
    // align the value colum right
    if (col == 2)
      return int(Qt::AlignRight | Qt::AlignVCenter);
    else
      return int(Qt::AlignLeft | Qt::AlignVCenter);
  }
  return QVariant();
}
