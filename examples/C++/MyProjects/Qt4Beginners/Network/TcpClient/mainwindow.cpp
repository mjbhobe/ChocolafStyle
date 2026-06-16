#include "mainwindow.h"
#include <QTcpSocket>
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow), connected_to_host_{false},
      socket_{nullptr}
{
  ui->setupUi(this);
}

MainWindow::~MainWindow() { delete ui; }

void MainWindow::printMessage(const QString &message)
{
  ui->chatDisplay->append(message);
}

void MainWindow::on_btnConnect_clicked()
{
  if (!connected_to_host_) {
    // create the socket & setup signals/slots
    socket_ = new QTcpSocket();
    connect(
        socket_, &QTcpSocket::connected, this, &MainWindow::socketConnected);
    connect(socket_, &QTcpSocket::disconnected, this,
        &MainWindow::socketDisconnected);
    connect(
        socket_, &QTcpSocket::readyRead, this, &MainWindow::socketReadyRead);
    // and connect to server
    socket_->connectToHost("127.0.0.1", 8001);
  }
  else {
    QString name = ui->txtName->text();
    QString text =
        QString("<font color=\"Orange\">%1 has left chat room!</font>")
            .arg(name);
    socket_->write(text.toUtf8());
    socket_->disconnectFromHost();
  }
}

void MainWindow::on_btnSend_clicked()
{
  QString name    = ui->txtName->text();
  QString message = ui->txtMessage->text();
  QString text =
      QString("<font color=\"blue\">%1: </font> %2").arg(name).arg(message);
  socket_->write(text.toUtf8());
  ui->txtMessage->clear();
  printMessage(text);
}

void MainWindow::socketConnected()
{
  // called when client socket connects to server
  qDebug() << "Connected to server";
  QString message =
      QString("<font color=\"green\">Connected to server!</font>");
  printMessage(message);
  QString name = ui->txtName->text();
  message = QString("<font color=\"purple\">%1 had joined chat room.</font>")
                .arg(name);
  socket_->write(message.toUtf8());
  printMessage(message);
  ui->txtName->setEnabled(false);
  ui->btnConnect->setText("Disconnect");
  connected_to_host_ = true;
}

void MainWindow::socketDisconnected()
{
  qDebug() << "Disconnected from server";
  printMessage("<font color=\"red\">Disconnected from server!</font>");
  ui->txtName->setEnabled(true);
  ui->btnConnect->setText("Connect");
  connected_to_host_ = false;
}

void MainWindow::socketReadyRead() { printMessage(socket_->readAll()); }

void MainWindow::on_txtMessage_textChanged(const QString &)
{
  // enable/disable Send button if txtMessage has/does-not-have text
  ui->btnSend->setEnabled(ui->txtMessage->text().length() > 0);
}

void MainWindow::on_txtName_textChanged(const QString &arg1)
{
  // enable/disable Connect button if txtName has/does-not-have text
  ui->btnConnect->setEnabled(ui->txtName->text().length() > 0);
}
