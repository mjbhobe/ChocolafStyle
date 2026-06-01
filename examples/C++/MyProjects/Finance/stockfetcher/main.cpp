#include <QApplication>
#include <curl/curl.h>
#include "MainWindow.h"

int main(int argc, char *argv[])
{
  // Global environment requirements layout for libcurl
  curl_global_init(CURL_GLOBAL_DEFAULT);

  QApplication app(argc, argv);
  MainWindow win;
  win.show();

  int execResult = app.exec();

  // Cleanup workspace cleanly before closing executable down
  curl_global_cleanup();
  return execResult;
}
