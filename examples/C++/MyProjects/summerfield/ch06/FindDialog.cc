// FindDialog.cc - find dialog implementation
#include <QtCore>
#include <QtWidgets>
#include "FindDialog.h"

FindDialog::FindDialog(QWidget *parent/*=nullptr*/)
   : QDialog(parent)
{
  namedLabel = new QLabel("Named:");
  namedLineEdit = new QLineEdit();
  lookInLabel = new QLabel("Look in:");
  lookInLineEdit = new QLineEdit();
  subfoldersCheckBox = new QCheckBox("Include Subfolders");
  tableWidget = new QTableWidget();
  messageLabel = new QLabel(QString("Built with Qt %1").arg(QT_VERSION_STR));

  findButton = new QPushButton("&Find");
  stopButton = new QPushButton("&Stop");
  closeButton = new QPushButton("&Close");
  helpButton = new QPushButton("&Help");

  setupUi();
}

void FindDialog::setupUi()
{
  QGridLayout *leftLayout = new QGridLayout;
  leftLayout->addWidget(namedLabel, 0, 0);
  leftLayout->addWidget(namedLineEdit, 0, 1);
  leftLayout->addWidget(lookInLabel, 1, 0);
  leftLayout->addWidget(lookInLineEdit, 1, 1);
  leftLayout->addWidget(subfoldersCheckBox, 2, 0, 1, 2);
  leftLayout->addWidget(tableWidget, 3, 0, 1, 2);
  leftLayout->addWidget(messageLabel, 4, 0, 1, 2);

  QVBoxLayout *rightLayout = new QVBoxLayout;
  rightLayout->addWidget(findButton);
  rightLayout->addWidget(stopButton);
  rightLayout->addWidget(closeButton);
  rightLayout->addStretch();
  rightLayout->addWidget(helpButton);

  QHBoxLayout *mainLayout = new QHBoxLayout();
  mainLayout->addLayout(leftLayout);
  mainLayout->addLayout(rightLayout);
  setLayout(mainLayout);

  setWindowTitle(tr("Find Files or Folders"));

  // setup signals & slots
  QObject::connect(closeButton, SIGNAL(clicked()), this, SLOT(close()));
}





