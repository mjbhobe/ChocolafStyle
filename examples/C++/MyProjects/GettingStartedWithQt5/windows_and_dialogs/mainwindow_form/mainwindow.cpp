#include "mainwindow.h"
#include <QAction>
#include <QApplication>
#include <QCloseEvent>
#include <QDate>
#include <QDateEdit>
#include <QFile>
#include <QFormLayout>
#include <QGridLayout>
#include <QHBoxLayout>
#include <QHeaderView>
#include <QLabel>
#include <QLineEdit>
#include <QLocale>
#include <QMainWindow>
#include <QMenuBar>
#include <QMessageBox>
#include <QPixmap>
#include <QPushButton>
#include <QRegularExpression>
#include <QRegularExpressionValidator>
#include <QStandardItemModel>
#include <QString>
#include <QTableView>
#include <QToolBar>
#include <QVBoxLayout>
#include <QWidget>
#include <print>
#include <tuple>

#ifndef IMAGES_PATH
#error "FATAL: IMAGES_PATH not defined on compiler command line!"
#endif

const std::string US_PHONE_REGEXP =
    R"(^(\+?1[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}$)";

const QString DATA_FILE_PATH = QString(IMAGES_PATH) + "/data.dat";

bool MainWindow::saveData()
{
  // Early check: Ensure table model is valid
  if (!m_tableModel) {
    return false;
  }

  // Save contents of our table model to DATA_FILE_PATH
  QFile file(DATA_FILE_PATH);
  if (!file.open(QIODevice::WriteOnly)) {
    return false;
  }

  QDataStream out(&file);
  out.setVersion(QDataStream::Qt_6_0);

  int rows = m_tableModel->rowCount();
  int cols = m_tableModel->columnCount();
  std::println("NOTE: table model has {} rows x {} cols", rows, cols);

  // 1. Write total grid dimensions
  out << rows << cols;
  if (out.status() != QDataStream::Ok) {
    file.close();
    return false;
  }

  // 2. Write header labels
  for (int c = 0; c < cols; ++c) {
    QStandardItem *header = m_tableModel->horizontalHeaderItem(c);
    if (header) {
      out << true;
      header->write(out);
      std::println("Wrote {} header item with title \"{}\"", c,
          header->text().toStdString());
    }
    else {
      out << false;
    }

    if (out.status() != QDataStream::Ok) {
      std::println("Error encountered when saving header items!");
      file.close();
      return false;
    }
  }

  // 3. Write grid cells
  for (int r = 0; r < rows; ++r) {
    for (int c = 0; c < cols; ++c) {
      QStandardItem *item = m_tableModel->item(r, c);
      if (item) {
        std::println(
            "Writing item at ({},{}) -> {}", r, c, item->text().toStdString());
        out << true;
        item->write(out); // Serializes text, roles, flags, check states
      }
      else {
        out << false; // Handles empty/uninitialized cells cleanly
      }

      if (out.status() != QDataStream::Ok) {
        std::println("Error writing item at ({},{}) -> {}", r, c,
            item->text().toStdString());
        file.close();
        return false;
      }
    }
  }

  file.close();

  // Final check: Verify file flush/close succeeded without device errors
  return file.error() == QFileDevice::NoError;
}

std::tuple<bool, QStandardItemModel *> MainWindow::loadData(
    QObject *parent /*=nullptr*/)
{
  // load contents of our table model to DATA_FILE_PATH
  std::println("Calling loadData()...");

  QFile file(DATA_FILE_PATH);
  if (!file.open(QIODevice::ReadOnly)) {
    std::println("Could not open file {}", DATA_FILE_PATH.toStdString());
    return {false, nullptr};
  }

  QDataStream in(&file);
  in.setVersion(QDataStream::Qt_6_0);

  // create a new model, which caller will set for QTableView
  auto model = new QStandardItemModel(parent);

  // Lambda helper for cleanup on read failure
  auto failAndCleanup = [&model]() -> std::tuple<bool, QStandardItemModel *> {
    delete model; // Clean up partially allocated model to prevent memory leaks
    return {false, nullptr};
  };

  int rows = 0;
  int cols = 0;

  // read and validate table dimensions
  in >> rows >> cols;
  if (in.status() != QDataStream::Ok || rows < 0 || cols < 0) {
    std::println("Failed to load table model dimensions!");
    return failAndCleanup();
  }
  else {
    std::println("Model has {} rows x {} cols", rows, cols);
  }

  model->setRowCount(rows);
  model->setColumnCount(cols);

  // read horizontal headers
  for (int c = 0; c < cols; ++c) {
    bool hasHeader = false;
    in >> hasHeader;
    if (in.status() != QDataStream::Ok) {
      return failAndCleanup();
    }

    if (hasHeader) {
      auto *header = new QStandardItem();
      header->read(in);
      if (in.status() != QDataStream::Ok) {
        std::println("Failed to load header!");
        delete header;
        return failAndCleanup();
      }
      model->setHorizontalHeaderItem(c, header);
    }
  }

  // read grid cells
  for (int r = 0; r < rows; ++r) {
    for (int c = 0; c < cols; ++c) {
      bool hasItem = false;
      in >> hasItem;
      if (in.status() != QDataStream::Ok) {
        return failAndCleanup();
      }

      if (hasItem) {
        auto *item = new QStandardItem();
        item->read(in);
        if (in.status() != QDataStream::Ok) {
          delete item;
          return failAndCleanup();
        }
        std::println(
            "Loaded item {} at ({},{}) item", item->text().toStdString(), r, c);
        model->setItem(r, c, item);
      }
    }
  }

  file.close();
  return {true, model};
}

MainWindow::MainWindow()
    : QMainWindow(), m_fileMenu{nullptr}, m_helpMenu{nullptr}
{
  // WARNING: don't change order of execution!!
  createActions();
  createMenus();
  createToolBar();
  setupCentralWidget();
}


void MainWindow::createActions()
{
  std::println("IMAGES_PATH = {}", IMAGES_PATH);
  QPixmap newIcon(QString(IMAGES_PATH) + "/file_new.png");
  QPixmap openIcon(QString(IMAGES_PATH) + "/file_open.png");
  QPixmap saveIcon(QString(IMAGES_PATH) + "/file_save.png");
  QPixmap clearIcon(QString(IMAGES_PATH) + "/clear.png");
  QPixmap exitIcon(QString(IMAGES_PATH) + "/exit.png");

  // file menu actions (dummy!)
  m_newAction = new QAction(newIcon, "&New", this);
  m_newAction->setShortcuts(QKeySequence::New);
  m_openAction = new QAction(openIcon, "&Open", this);
  m_openAction->setShortcuts(QKeySequence::Open);
  // only quit works!
  m_quitAction = new QAction(exitIcon, "&Quit", this);
  m_quitAction->setShortcuts(QKeySequence::Quit);

  // help menu actions
  m_aboutAction = new QAction("About...", this);
  m_aboutAction->setShortcut(QKeySequence(Qt::CTRL + Qt::Key_H)); // Ctrl+H

  // other actions
  m_saveAction = new QAction(saveIcon, "&Save", this);
  m_clearAction = new QAction(clearIcon, "Clear &all", this);

  // setup signals & slots
  QObject::connect(
      m_newAction, &QAction::triggered, this, &MainWindow::fileNew);
  QObject::connect(
      m_openAction, &QAction::triggered, this, &MainWindow::fileOpen);
  QObject::connect(
      m_quitAction, &QAction::triggered, this, &QApplication::quit);
  QObject::connect(
      m_aboutAction, &QAction::triggered, this, &MainWindow::about);
  QObject::connect(
      m_saveAction, &QAction::triggered, this, &MainWindow::saveRecord);
  QObject::connect(
      m_clearAction, &QAction::triggered, this, &MainWindow::clearFields);
}

void MainWindow::createMenus()
{
  // create the File Menu
  m_fileMenu = menuBar()->addMenu("&File");
  m_fileMenu->addAction(m_newAction);
  m_fileMenu->addAction(m_openAction);
  m_fileMenu->addSeparator();
  m_fileMenu->addAction(m_quitAction);

  // the help menu
  m_helpMenu = menuBar()->addMenu("&Help");
  m_helpMenu->addAction(m_aboutAction);
}

void MainWindow::createToolBar()
{
  // setup toolbar
  m_toolBar = addToolBar("Main Toolbar");
  m_toolBar->addAction(m_newAction);
  m_toolBar->addAction(m_openAction);
  m_toolBar->addSeparator();
  m_toolBar->addAction(m_clearAction);
  m_toolBar->addAction(m_quitAction);
}

void MainWindow::setupCentralWidget()
{
  m_centralWidget = new QWidget();
  // main layout
  QVBoxLayout *vbox = new QVBoxLayout;
  // upper part - data entry part
  QVBoxLayout *form = createDataEntryForm();
  // lower part with QTableView
  QTableView *tableView = createTableView();

  vbox->addLayout(form);
  vbox->addWidget(tableView);

  m_centralWidget->setLayout(vbox);
  setCentralWidget(m_centralWidget);
}

void MainWindow::applyLocaleWith4DigitYear(QDateEdit *dateEdit)
{
  // get the local date format string from current system/Qt locale
  QLocale currentLocale = QLocale::system();
  QString formatPattern = currentLocale.dateFormat(QLocale::ShortFormat);

  // Replace any standalone 'yy' (2-digit year) with 'yyyy' (4-digit year)
  // Avoid replacing 'yyyy' if it already exists
  if (!formatPattern.contains("yyyy")) {
    formatPattern.replace("yy", "yyyy");
  }

  // Set the updated format and active locale on the QDateEdit widget
  dateEdit->setLocale(currentLocale);
  dateEdit->setDisplayFormat(formatPattern);
}

QVBoxLayout *MainWindow::createDataEntryForm()
{
  // data entry form (as QFormLayout)
  // top half of vbox layout
  QLabel *name = new QLabel("Name: ");
  m_txtName = new QLineEdit();
  m_txtName->setPlaceholderText("Enter your name");
  QLabel *dob = new QLabel("Date Of Birth:");
  m_txtDob = new QDateEdit(this);
  m_txtDob->setCalendarPopup(true); // force calendar rather than spinner
  m_txtDob->setDate(QDate::currentDate());
  applyLocaleWith4DigitYear(m_txtDob); // force 4 digit date entry
  QLabel *phone = new QLabel("Phone: ");
  m_txtPhoneNo = new QLineEdit;
  m_txtPhoneNo->setPlaceholderText("Enter your phone number");
  QRegularExpression phoneRegex =
      QRegularExpression(QString::fromStdString(US_PHONE_REGEXP));
  QRegularExpressionValidator *phone_validator =
      new QRegularExpressionValidator(phoneRegex, m_txtPhoneNo);
  m_txtPhoneNo->setValidator(phone_validator);

  // layout all data entry widgets in a 3 x 3 grid
  QGridLayout *form = new QGridLayout();
  form->addWidget(name, 0, 0);
  form->addWidget(m_txtName, 0, 1);
  form->addWidget(dob, 1, 0);
  form->addWidget(m_txtDob, 1, 1);
  form->addWidget(phone, 2, 0);
  form->addWidget(m_txtPhoneNo, 2, 1);

  // add a button panel below (horz layout)
  m_btnSave = new QPushButton(this);
  m_btnSave->setText(m_saveAction->text());
  m_btnSave->setIcon(m_saveAction->icon());
  m_btnSave->setToolTip("Save Record");
  m_btnSave->setEnabled(false);
  QObject::connect(
      m_btnSave, &QPushButton::clicked, this, &MainWindow::saveRecord);
  QObject::connect(
      m_txtName, &QLineEdit::textChanged, this, &MainWindow::enableDisableSave);
  QObject::connect(m_txtPhoneNo, &QLineEdit::textChanged, this,
      &MainWindow::enableDisableSave);
  m_btnClearAll = new QPushButton(this);
  m_btnClearAll->setText(m_clearAction->text());
  m_btnClearAll->setIcon(m_clearAction->icon());
  m_btnClearAll->setToolTip("Clear All Fields");
  QObject::connect(
      m_btnClearAll, &QPushButton::clicked, this, &MainWindow::clearFields);
  QHBoxLayout *hbox = new QHBoxLayout();
  hbox->addStretch();
  hbox->addWidget(m_btnSave);
  hbox->addWidget(m_btnClearAll);

  QVBoxLayout *vbox2 = new QVBoxLayout();
  vbox2->addLayout(form);
  vbox2->addLayout(hbox);
  return vbox2;
}

QTableView *MainWindow::createTableView()
{
  // create the table view & associated buttons
  // that are placed on bottom half of clieny area
  m_tableView = new QTableView();
  m_tableView->setContextMenuPolicy(Qt::CustomContextMenu);
  m_tableView->horizontalHeader()->setSectionResizeMode(
      QHeaderView::ResizeMode::Stretch);
  auto [success, model] = loadData();
  if (!success) {
    // no data saved previously or error in loading data
    // use defaults
    std::println(
        "Could not load data, using default settings for table model!");
    m_tableModel = new QStandardItemModel(1, 3, this);
    m_tableModel->setHorizontalHeaderItem(
        0, new QStandardItem(QString("Name")));
    m_tableModel->setHorizontalHeaderItem(
        1, new QStandardItem(QString("Date of Birth")));
    m_tableModel->setHorizontalHeaderItem(
        2, new QStandardItem(QString("Phone Number")));
  }
  else {
    std::println("Model loaded successfully! Setting model from data");
    m_tableModel = model;
  }
  m_tableView->setModel(m_tableModel);
  // add a dummy row to table
  QStandardItem *nameItem = new QStandardItem("Manish B");
  QDate dob(1969, 6, 22);
  QStandardItem *dobItem = new QStandardItem(dob.toString());
  QStandardItem *phoneItem = new QStandardItem("9325642112");
  m_tableModel->setItem(0, 0, nameItem);
  m_tableModel->setItem(0, 1, dobItem);
  m_tableModel->setItem(0, 2, phoneItem);


  return m_tableView;
}

void MainWindow::closeEvent(QCloseEvent *e)
{
  std::println("MainWindow::closeEvent() called...");
  bool ret = saveData();
  std::println("saveData() returned {}", (ret ? "true" : "false"));
  e->accept();
  // saveData() ? e->accept() : e->ignore();
}

void MainWindow::about()
{
  // Title of the dialog
  QString title = windowTitle();

  // Rich text / HTML content for the body
  constexpr std::string_view rawHtmlTemplate = R"(
      <h3>My Qt Application v1.0.0</h3>
      <p>Developed with C++20 and Qt{}.</p>
      <p>Copyright &copy; 2026 Manish Bhobe. All rights reserved.</p>
      <p>Visit our website: <a href='https://namostute.com'>namostute.com</a></p>
  )";
  std::string text = std::format(rawHtmlTemplate, QT_VERSION_STR);

  // Display the about box
  QMessageBox::about(this, title, QString::fromStdString(text));
}

void MainWindow::fileNew()
{
  QMessageBox::information(this, windowTitle(),
      QString("You clicked File->New\nYet to be implemented!"));
}

void MainWindow::fileOpen()
{
  QMessageBox::information(this, windowTitle(),
      QString("You clicked File->Open\nYet to be implemented!"));
}

void MainWindow::saveRecord()
{
  QStandardItem *nameItem = new QStandardItem(m_txtName->text());
  QDate dob(1969, 6, 22);
  QStandardItem *dobItem = new QStandardItem(m_txtDob->date().toString());
  QStandardItem *phoneItem = new QStandardItem(m_txtPhoneNo->text());
  m_tableModel->appendRow({nameItem, dobItem, phoneItem});
  clearFields();
}

void MainWindow::clearFields()
{
  m_txtName->clear();
  m_txtDob->setDate(QDate::currentDate());
  m_txtPhoneNo->clear();
}

void MainWindow::enableDisableSave()
{
  // enable save when values entered in all form fields
  // else keep it disables
  bool enabled = (!m_txtName->text().isEmpty() && !m_txtDob->text().isEmpty() &&
      !m_txtPhoneNo->text().isEmpty());
  m_btnSave->setEnabled(enabled);
}
