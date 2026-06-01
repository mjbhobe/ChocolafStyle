#include <QHeaderView>
#include <QScrollBar>
#include "MainWindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
  setWindowTitle("Asset Valuation Dashboard");
  resize(900, 500);

  m_mainTableView   = new QTableView(this);
  m_frozenTableView = new QTableView(this);
  m_model           = new PortfolioModel(this);

  setCentralWidget(m_mainTableView);
}

void MainWindow::initializeData(const std::map<QString, int> &portfolio, const QDate &start, const QDate &end,
    const std::map<QString, std::vector<std::pair<QDate, double>>> &rawData)
{
  // Collect all chronological dates across tickers
  std::vector<QDate> uniqueDates;
  for (QDate d = start; d <= end; d = d.addDays(1)) {
    // Cycle files and verify if any stock has transactional pricing records on this day
    for (const auto &[ticker, history]: rawData) {
      for (const auto &[itemDate, price]: history) {
        if (itemDate == d && std::find(uniqueDates.begin(), uniqueDates.end(), d) == uniqueDates.end()) {
          uniqueDates.push_back(d);
        }
      }
    }
  }
  std::sort(uniqueDates.begin(), uniqueDates.end());

  m_model->populateData(portfolio, uniqueDates, rawData);

  m_mainTableView->setModel(m_model);
  m_frozenTableView->setModel(m_model);

  setupFrozenColumnsLayout();
}

void MainWindow::setupFrozenColumnsLayout()
{
  // Configure the frozen overlay frame look
  m_frozenTableView->setFocusPolicy(Qt::NoFocus);
  m_frozenTableView->verticalHeader()->hide();
  m_frozenTableView->horizontalHeader()->setSectionResizeMode(QHeaderView::Fixed);

  m_mainTableView->verticalHeader()->hide();

  // Attach overlay viewport context boundaries on top of parent container layout
  m_mainTableView->viewport()->stackUnder(m_frozenTableView);

  // Hide everything past the first two columns on the frozen overlay
  for (int col = 2; col < m_model->columnCount(); ++col) {
    m_frozenTableView->setColumnHidden(col, true);
  }

  // Set fixed widths for the frozen columns
  m_mainTableView->setColumnWidth(0, 140);
  m_mainTableView->setColumnWidth(1, 100);
  m_frozenTableView->setColumnWidth(0, 140);
  m_frozenTableView->setColumnWidth(1, 100);

  // Freeze scrollbars on overlay
  m_frozenTableView->setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  m_frozenTableView->setVerticalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
  m_frozenTableView->show();

  // Align row geometry layouts
  m_frozenTableView->horizontalHeader()->setFixedHeight(m_mainTableView->horizontalHeader()->height());

  // Sync table layout placement sizing values
  auto updateGeometryLambda = [this]() {
    m_frozenTableView->setGeometry(m_mainTableView->frameWidth(), m_mainTableView->frameWidth(),
        m_mainTableView->columnWidth(0) + m_mainTableView->columnWidth(1),
        m_mainTableView->viewport()->height() + m_mainTableView->horizontalHeader()->height());
  };

  // Wire up listeners to guarantee identical vertical scrolling adjustments between components
  connect(m_mainTableView->verticalScrollBar(), &QScrollBar::valueChanged,
      m_frozenTableView->verticalScrollBar(), &QScrollBar::setValue);
  connect(m_frozenTableView->verticalScrollBar(), &QScrollBar::valueChanged,
      m_mainTableView->verticalScrollBar(), &QScrollBar::setValue);

  connect(m_mainTableView->horizontalHeader(), &QHeaderView::geometriesChanged, this, updateGeometryLambda);
  connect(m_mainTableView->verticalHeader(), &QHeaderView::geometriesChanged, this, updateGeometryLambda);

  updateGeometryLambda();
}
