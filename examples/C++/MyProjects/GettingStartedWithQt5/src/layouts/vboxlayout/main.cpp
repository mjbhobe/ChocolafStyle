// ==================================================================================
// VBox Layout - laying out widgets in a verticle box layout
//
// @author: Manish Bhobe
// My Experiments with C/C++, Qt Framework and STL
// Code shared for learning purposes only. Use at your own risk!
// ==================================================================================
#include <QApplication>
#include <QComboBox>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>

int main(int argc, char **argv)
{
  QApplication app(argc, argv);

  // create the GUI
  QWidget widget;
  widget.setWindowTitle("Qt Demos | QVBoxLayout Demo");

  QLabel *userId = new QLabel("Username");
  QLineEdit *txtUserId = new QLineEdit();
  QLabel *password = new QLabel("Password");
  QLineEdit *txtPassword = new QLineEdit();
  txtPassword->setEchoMode(QLineEdit::EchoMode::Password);
  QPushButton *btnLogin = new QPushButton("Login");
  btnLogin->setDefault(true);
  QPushButton *btnRegister = new QPushButton("Register");

  QVBoxLayout *layout = new QVBoxLayout();
  layout->addWidget(userId);
  layout->addWidget(txtUserId);
  layout->addWidget(password);
  layout->addWidget(txtPassword);
  QHBoxLayout *hbox = new QHBoxLayout();
  hbox->setAlignment(Qt::AlignmentFlag::AlignRight);
  hbox->addWidget(btnLogin);
  hbox->addWidget(btnRegister);
  layout->addLayout(hbox);
  widget.setLayout(layout);

  widget.setMinimumWidth(400);
  widget.show();

  return app.exec();
}
