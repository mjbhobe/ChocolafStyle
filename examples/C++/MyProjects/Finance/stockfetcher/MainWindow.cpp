#include <QHeaderView>
#include <QMessageBox>
#include "DataFetcher.h"
#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
  setWindowTitle("Yahoo Finance Data Viewer");
  resize(750, 500);

  m_tableView = new QTableView(this);
  m_model     = new StockModel(this);

  m_tableView->setModel(m_model);
  m_tableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Stretch);
  setCentralWidget(m_tableView);

  // Dynamic general configurations: Change your parameters right here!
  QString startStr = "01-Apr-2026";
  QString endStr   = "31-May-2026";

  // Pass timestamps downstream seamlessly
  DataFetcher *fetcherReliance = new DataFetcher("RELIANCE.NS", startStr, endStr, this);
  DataFetcher *fetcherITC      = new DataFetcher("ITC.NS", startStr, endStr, this);

  connect(fetcherReliance, &DataFetcher::dataFetched, this, &MainWindow::handleData);
  connect(fetcherReliance, &DataFetcher::errorOccurred, this, &MainWindow::handleError);
  connect(fetcherITC, &DataFetcher::dataFetched, this, &MainWindow::handleData);
  connect(fetcherITC, &DataFetcher::errorOccurred, this, &MainWindow::handleError);

  connect(fetcherReliance, &DataFetcher::finished, fetcherReliance, &DataFetcher::deleteLater);
  connect(fetcherITC, &DataFetcher::finished, fetcherITC, &DataFetcher::deleteLater);

  fetcherReliance->start();
  fetcherITC->start();
}

void MainWindow::handleData(QString ticker, std::vector<std::pair<QDate, double>> data)
{
  m_model->updateData(ticker, data);
}

void MainWindow::handleError(QString msg) { QMessageBox::critical(this, "Application Failure", msg); }
