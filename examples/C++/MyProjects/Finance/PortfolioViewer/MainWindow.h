#pragma once
#include <QMainWindow>
#include <QTableView>
#include "PortfolioModel.h"

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    explicit MainWindow(QWidget *parent = nullptr);

    void initializeData(const std::map<QString, int> &portfolio, const QDate &start, const QDate &end,
        const std::map<QString, std::vector<std::pair<QDate, double>>> &rawData);
  private:
    QTableView *m_mainTableView;
    QTableView *m_frozenTableView; // Internal twin frame to handle non-scrollable area
    PortfolioModel *m_model;

    void setupFrozenColumnsLayout();
};
