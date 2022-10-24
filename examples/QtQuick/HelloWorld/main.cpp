#include "chocolaf.h"
#include <QGuiApplication>
#include <QQmlApplicationEngine>

int main(int argc, char *argv[])
{
   Chocolaf::ChocolafApp::setupForHighDpiScreens();
   Chocolaf::ChocolafApp app(argc, argv);
   app.setStyle("Chocolaf");

   // QGuiApplication app(argc, argv);

   QQmlApplicationEngine engine;
   const QUrl url(u"qrc:/HelloWorld/main.qml"_qs);
   QObject::connect(
         &engine, &QQmlApplicationEngine::objectCreated, &app,
         [url](QObject *obj, const QUrl &objUrl) {
            if (!obj && url == objUrl)
               QCoreApplication::exit(-1);
         },
         Qt::QueuedConnection);
   engine.load(url);

   return app.exec();
}
