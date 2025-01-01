#ifndef __SysmetsModel_h__
#define __SysmetsModel_h__

#include "Sysmets.h"
#include <QAbstractTableModel>

class SysmetsModel : public QAbstractTableModel {
  Q_OBJECT
public:
  explicit SysmetsModel(QObject* parent = nullptr);

  int rowCount(const QModelIndex& parent = QModelIndex()) const override;
  int columnCount(const QModelIndex& parent = QModelIndex()) const override;
  QVariant headerData(
    int section, Qt::Orientation orientation, int role = Qt::DisplayRole) const override;
  QVariant data(const QModelIndex& index, int role = Qt::DisplayRole) const override;
};

#endif // __SysmetsModel_h__
