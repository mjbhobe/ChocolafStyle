#include "server.h"

Server::Server(QObject *parent)
    : QObject{parent}, chat_server_{nullptr}, all_clients_{nullptr}
{}

void Server::startServer()
{
  all_clients_ = new QVector<QTcpSocket *>();
  chat_server_ = new QTcpServer();
  chat_server_->setMaxPendingConnections(10);
  QObject::connect(chat_server_, &QTcpServer::newConnection, this,
      &Server::newClientConnection);
  // listen on port 8001
  if (chat_server_->listen(QHostAddress::Any, 8001)) {
    qDebug() << "Server started. Listening on port 8001";
  }
  else {
    qDebug() << "Server failed to start! Error: "
             << chat_server_->errorString();
  }
}

void Server::sendMessageToClients(const QString &message)
{
  if (all_clients_->size() > 0) {
    // server has some clients
    for (QTcpSocket *client: *all_clients_) {
      if (client->isOpen() && client->isWritable())
        client->write(message.toUtf8());
    }
  }
}

void Server::newClientConnection()
{
  QTcpSocket *client = chat_server_->nextPendingConnection();
  QString ipAddress  = client->peerAddress().toString();
  int port           = client->peerPort();
  qDebug() << "New connection from " << ipAddress << " on port " << port;
  // setup slots for the new connection
  connect(client, &QTcpSocket::disconnected, this, &Server::socketDisconnected);
  connect(client, &QTcpSocket::readyRead, this, &Server::socketReadReady);
  connect(client, &QTcpSocket::stateChanged, this, &Server::socketStateChanged);
  all_clients_->push_back(client);
}

void Server::socketDisconnected()
{
  // who sent this signal?
  QTcpSocket *client = qobject_cast<QTcpSocket *>(QObject::sender());
  QString ipAddress  = client->peerAddress().toString();
  int port           = client->peerPort();
  qDebug() << "Disconnected client from " << ipAddress << " on port " << port;
}

void Server::socketReadReady()
{
  // this function is triggered when a client sends a message
  // we just read the message & display it
  QTcpSocket *client = qobject_cast<QTcpSocket *>(QObject::sender());
  QString ipAddress  = client->peerAddress().toString();
  int port           = client->peerPort();
  QString data       = QString(client->readAll());
  qDebug() << "Received message (" << data << ") from client at " << ipAddress
           << " on port " << port;
}

void Server::socketStateChanged(QAbstractSocket::SocketState state)
{
  // this functon/slot is called when networking state of client is changed
  QTcpSocket *client = qobject_cast<QTcpSocket *>(QObject::sender());
  QString ipAddress  = client->peerAddress().toString();
  int port           = client->peerPort();
  // find out what changed....
  QString desc;
  if (state == QAbstractSocket::UnconnectedState)
    desc = "The socket is not connected.";
  else if (state == QAbstractSocket::HostLookupState)
    desc = "The socket is performing a host name lookup.";
  else if (state == QAbstractSocket::ConnectingState)
    desc = "The socket has started establishing a connection.";
  else if (state == QAbstractSocket::ConnectedState)
    desc = "A connection is established.";
  else if (state == QAbstractSocket::BoundState)
    desc = "The socket is bound to an address and port.";
  else if (state == QAbstractSocket::ClosingState)
    desc = "The socket is about to close (data may still be waiting to be "
           "written).";
  else if (state == QAbstractSocket::ListeningState)
    desc = "For internal use only.";

  qDebug() << "Socket state changed at " << ipAddress << " on port " << port
           << " : " << desc;
}
