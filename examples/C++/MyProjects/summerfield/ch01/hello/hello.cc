// hello.cc: Hello World with Qt
#include <QApplication>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QVBoxLayout>

int main(int argc, char **argv)
{
    QApplication app(argc, argv);
    QApplication::setFont(QApplication::font("QMenu"));
    app.setStyle("Fusion");

    // create & show our GUI
    QWidget window;
    window.setWindowTitle("Hello Qt World");
    QVBoxLayout *l = new QVBoxLayout();
    QHBoxLayout *w = new QHBoxLayout;
    QLabel *hello = new QLabel("Welcome to Qt programming. Enjoy the ride!");
    QPushButton *quit = new QPushButton("Quit!");
    quit->setToolTip("Quit Application");
    w->addWidget(hello);
    w->addWidget(quit);
    l->addLayout(w);
    window.setLayout(l);

    // connect signals & slots
    QObject::connect(quit, SIGNAL(clicked()), qApp, SLOT(quit()));

    window.show();

    return app.exec();
}
