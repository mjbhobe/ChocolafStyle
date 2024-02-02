#include "mainwin.h"
#include "findDialog.h"
#include "gotocelldialog.h"
#include <QDebug>
#include <QPushButton>
#include <QVBoxLayout>

MainWin::MainWin(QWidget *parent) : QWidget{parent}
{
  setWindowTitle("Dialogs Tester");
  auto msg = new QLabel("Click buttons below to launch dialogs");
  callFindDialog = new QPushButton("Call Find Dialog");
  callGotoCellDialog = new QPushButton("Call GoToCell Dialog");

  auto layout = new QVBoxLayout;
  layout->addWidget(msg);
  layout->addWidget(callFindDialog);
  layout->addWidget(callGotoCellDialog);
  setLayout(layout);

  QObject::connect(callFindDialog, SIGNAL(clicked()), this,
                   SLOT(findDialogButtonClicked()));
  QObject::connect(callGotoCellDialog, SIGNAL(clicked()), this,
                   SLOT(gotoCellDialogButtonClicked()));
}

void MainWin::findDialogButtonClicked()
{
  auto findDialog = new FindDialog(this);
  findDialog->setFont(QApplication::font("QMenu"));

  // connect signals & slots
  connect(findDialog, &FindDialog::findNext,
          [=](const QString &str, Qt::CaseSensitivity cs, bool wwo) {
            qDebug() << "Search FORWARD for: " << str
                     << " case sensitive: " << (cs == Qt::CaseSensitive ? "Yes" : "No")
                     << " whole words only: " << (wwo ? "Yes" : "No");
          });
  // connect signals & slots
  connect(findDialog, &FindDialog::findPrevious,
          [=](const QString &str, Qt::CaseSensitivity cs, bool wwo) {
            qDebug() << "Search BACKWARD for: " << str
                     << " case sensitive: " << (cs == Qt::CaseSensitive ? "Yes" : "No")
                     << " whole words only: " << (wwo ? "Yes" : "No");
          });

  findDialog->show();
}

void MainWin::gotoCellDialogButtonClicked()
{
  auto gotoCellDialog = new GoToCellDialog();
  if (gotoCellDialog->exec() == QDialog::Accepted) {
    qDebug() << "Will jump to cell " << gotoCellDialog->lineEdit->text();
  } else {
    qDebug() << "You Cancelled the dialog";
  }
}
