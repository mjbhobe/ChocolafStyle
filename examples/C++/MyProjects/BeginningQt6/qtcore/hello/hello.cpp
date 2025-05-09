#include <print>
#include <QtCore>

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);

  std::println(std::format("Hello! Welcome to Qt programming.\n"
        "You are using Qt {}", QT_VERSION_STR);
  return EXIT_SUCCESS;
}
