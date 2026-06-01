#pragma once
#include <QMainWindow>
#include <QTableView>
#include "StockModel.h"

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    explicit MainWindow(QWidget *parent = nullptr);

  private slots:
    void handleData(QString ticker, std::vector<std::pair<QDate, double>> data);
    void handleError(QString msg);
  private:
    QTableView *m_tableView;
    StockModel *m_model;
};
