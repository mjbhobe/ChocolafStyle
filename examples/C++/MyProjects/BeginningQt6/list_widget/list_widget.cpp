// list_widget.cpp: implementation of MainWidget class
#include "list_widget.h"
#include "QtAwesome.h"
#include "qactionpushbtn.h"
#include <QAction>
#include <QApplication>
#include <QHBoxLayout>
#include <QIcon>
#include <QInputDialog>
#include <QListWidget>
#include <QMessageBox>
#include <QPushButton>
#include <QStringList>
#include <QToolTip>
#include <QVBoxLayout>
#include <QVariantMap>
#include <QWidget>
#include <fmt/core.h>

MainWidget::MainWidget(QWidget *parent /*=nullptr*/) : QWidget(parent) {
  setMinimumSize(400, 200);
  _list_widget = new QListWidget();
  initializeUi();
}

void MainWidget::initializeUi() {
  _list_widget->setAlternatingRowColors(true);
  QStringList grocery_list = {
      "grapes", "broccoli", "garlic", "cheese", "bacon",
      "eggs",   "waffles",  "rice",   "soda",
  };

  foreach (QString item, grocery_list) {
    QListWidgetItem *lwitem = new QListWidgetItem();
    lwitem->setText(item);
    _list_widget->addItem(lwitem);
  }

  createActions();

  // QPushButton *add_btn = new QPushButton("Add");
  // add_btn->addAction(_addAction);
  QActionPushBtn *add_btn = new QActionPushBtn(_addAction, this);
  // add_btn->setToolTip("Add a new item");
  QPushButton *insert_btn = new QPushButton("Insert");
  insert_btn->setToolTip("Insert new item at location");
  QPushButton *remove_btn = new QPushButton("Remove");
  remove_btn->setToolTip("Remove selected item");
  QPushButton *clear_btn = new QPushButton("Clear");
  clear_btn->setToolTip("Clear all grocery items");
  QPushButton *exit_btn = new QPushButton("Exit");
  exit_btn->setToolTip("Quit Application");

  QVBoxLayout *btn_layout = new QVBoxLayout;
  btn_layout->addWidget(add_btn);
  btn_layout->addWidget(insert_btn);
  btn_layout->addWidget(remove_btn);
  btn_layout->addWidget(clear_btn);
  btn_layout->addWidget(exit_btn);

  QHBoxLayout *layout = new QHBoxLayout;
  layout->addWidget(_list_widget);
  layout->addLayout(btn_layout);
  setLayout(layout);

  // signals & slots
  QObject::connect(add_btn, SIGNAL(clicked()), this, SLOT(addItem()));
  QObject::connect(exit_btn, SIGNAL(clicked()), qApp, SLOT(quit()));
}

void MainWidget::createActions() {
  fa::QtAwesome *awesome = new fa::QtAwesome(this);
  awesome->initFontAwesome();

  QVariantMap options{};
  QColor color_active = this->palette().color(QPalette::Highlight);
  options.insert("color_active", color_active);

  auto add_icon = awesome->icon(fa::fa_regular, fa::fa_plus, options);
  _addAction = new QAction(add_icon, tr("&Add Item"), this);
  _addAction->setShortcut(tr("Ctrl+N"));
  _addAction->setStatusTip("Add a new item to the basket");
  _addAction->setToolTip("Add New Item");
  QObject::connect(_addAction, SIGNAL(triggered()), this, SLOT(addItem()));
}

void MainWidget::addItem() {
  bool ok;
  QString text = QInputDialog::getText(this, tr("Add Item"), tr("New Item"),
                                       QLineEdit::Normal, "", &ok);
  if (ok && !text.isEmpty()) {
    // add to end of list if not already present
    text = text.toLower();
    auto items = _list_widget->findItems(text, Qt::MatchExactly);
    if (items.isEmpty()) {
      QListWidgetItem *item = new QListWidgetItem();
      item->setText(text);
      _list_widget->addItem(item);
    } else {
      QMessageBox::information(
          this, "Add Item",
          fmt::format("This item \'{}\' already exists in list!",
                      text.toStdString().c_str())
              .c_str());
    }
  }
}

void MainWidget::insertItem() {}

void MainWidget::removeItem() {}

void MainWidget::clearItems() {}
