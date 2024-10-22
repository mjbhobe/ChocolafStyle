// #include <QCoreApplication>
#include "gmp.h"
#include <QCoreApplication>
#include <QDebug>
#include <QDir>
#include <QFile>
#include <QStandardPaths>
#include <QStringList>
#include <QTextStream>

// DON'T USE <iostream> - all other std includes & data structures are Ok!
static QTextStream cout(stdout, QIODevice::WriteOnly);

QString factorial(unsigned long num)
{
  mpz_t mpz_fact;

  // initialize mpz with all 0
  mpz_init_set_ui(mpz_fact, 0);
  // calculate factorial of num into mpz_fac
  mpz_fac_ui(mpz_fact, num);
  // convert mpz_fac to char*
  char *buff = new char[mpz_sizeinbase(mpz_fact, 10) + 2];
  mpz_get_str(buff, 10, mpz_fact);
  // and convert to QString
  QString ret(buff);
  delete[] buff;

  return ret;
}

int main(int argc, char **argv)
{
  QCoreApplication app(argc, argv);

  QDir dir1("c:/qt"), dir2("c:/dev/qt");

  cout << dir1.path() << " exists? " << dir1.exists() << Qt::endl;
  cout << dir2.path() << " exists? " << dir2.exists() << Qt::endl;
  QDir dir3; // defaults to /
  cout << "Drives in root file system..." << Qt::endl;
  foreach (QFileInfo item, dir3.drives())
    cout << item.absoluteFilePath() << Qt::endl;

  // list all contents of the pictures folder
  const QStringList picsLocation = QStandardPaths::standardLocations(
      QStandardPaths::PicturesLocation);
  QDir picsDir = picsLocation.isEmpty() ? QDir::currentPath() : QDir(picsLocation.last());
  picsDir.setFilter(QDir::AllDirs | QDir::NoDotAndDotDot | QDir::Files);
  picsDir.setSorting(QDir::DirsFirst | QDir::Size);
  cout << "Listing contents of " << picsDir.absolutePath() << Qt::endl;

  QFileInfoList imageFiles = picsDir.entryInfoList();
  foreach (QFileInfo imageFileInfo, imageFiles) {
    cout << (imageFileInfo.isDir() ? "Dir: " : "File: ");
    cout << imageFileInfo.absoluteFilePath();
    if (!imageFileInfo.isDir())
      cout << " " << static_cast<int>(imageFileInfo.size() / 1000) << " Kb";
    cout << Qt::endl;
  }

  // return app.exec();
  return 0;
}
