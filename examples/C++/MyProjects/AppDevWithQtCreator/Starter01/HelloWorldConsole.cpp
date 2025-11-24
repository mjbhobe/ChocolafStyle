// HelloWorldConsole.cpp - Hello World with Qt - Console app
// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <QCoreApplication>
#include <print>

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);

  std::println("Hello World! Welcome to Qt {}", QT_VERSION_STR);

  return app.exec();
}
