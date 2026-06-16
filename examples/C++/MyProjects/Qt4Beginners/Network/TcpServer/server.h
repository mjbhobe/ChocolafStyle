#ifndef SERVER_H
#define SERVER_H

#include <QDebug>
#include <QObject>
#include <QTcpServer>
#include <QTcpSocket>
#include <QVector>

class Server : public QObject {
    Q_OBJECT
  public:
    explicit Server(QObject *parent = nullptr);
    void startServer();
    void sendMessageToClients(const QString &message);

  public slots:
    // add slots here
    void newClientConnection();
    void socketDisconnected();
    void socketReadReady();
    void socketStateChanged(QAbstractSocket::SocketState state);

  signals:
    // add signals here
  private:
    QTcpServer *chat_server_;
    QVector<QTcpSocket *> *all_clients_;
};

#endif // SERVER_H
