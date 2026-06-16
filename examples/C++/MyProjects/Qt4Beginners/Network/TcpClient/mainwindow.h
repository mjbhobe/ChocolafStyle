#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QDebug>
#include <QMainWindow>
#include <QTcpSocket>

QT_BEGIN_NAMESPACE
namespace Ui {
  class MainWindow;
}
QT_END_NAMESPACE

class MainWindow : public QMainWindow {
    Q_OBJECT
  public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow() override;
    void printMessage(const QString &message);
  private slots:
    // for form elements
    void on_btnConnect_clicked();
    void on_btnSend_clicked();
    // custom
    void socketConnected();
    void socketDisconnected();
    void socketReadyRead();
    void on_txtMessage_textChanged(const QString &arg1);
    void on_txtName_textChanged(const QString &arg1);
  private:
    Ui::MainWindow *ui;
    bool connected_to_host_;
    QTcpSocket *socket_;
};
#endif // MAINWINDOW_H
