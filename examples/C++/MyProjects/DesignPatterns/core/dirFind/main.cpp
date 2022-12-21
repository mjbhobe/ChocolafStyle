#include <cstdlib>
#include <QCoreApplication>
#include <QDir>
#include <QFileInfo>
#include <QStringList>
#include <QTextStream>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

#ifdef Q_OS_WINDOWS
const QString CODE_DIR = QString("C:/Dev/Code/git-projects/ChocolafStyle/examples/"
                                 "C++/MyProjects");
#else
const QString CODE_DIR = QString("/home/mjbhobe/code/git-projects/ChocolafStyle/examples/"
                                 "C++/MyProjects");
#endif

void findFiles(QDir d, QStringList &matchingFiles, const QString suffix = "cpp",
               bool recursive = true, bool symLinks = false)
{
   d.setSorting(QDir::Name); // sort list by name of directory
   QDir::Filters df = QDir::Files | QDir::NoDotAndDotDot;
   if (recursive)
      df |= QDir::Dirs;
   if (not symLinks)
      df |= QDir::NoSymLinks;
   // get list of all matches (files & directories)
   QStringList qsl = d.entryList(df, QDir::Name | QDir::DirsFirst);
   foreach (const QString &entry, qsl) {
      QFileInfo finfo(d, entry);
      if (finfo.isDir()) {
         // recurse into dir
         QDir sd(finfo.absoluteFilePath());
         findFiles(sd, matchingFiles, suffix, recursive, symLinks);
      }
      else {
         if (finfo.completeSuffix() == suffix)
            matchingFiles.append(finfo.absoluteFilePath());
      }
   }
}

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);
   QDir dir = QDir(CODE_DIR);
   if (!dir.exists()) {
      cerr << "FATAL: search directory " << dir.path() << " does not exist!" << Qt::endl;
      return EXIT_FAILURE;
   }
   else {
      QStringList matchingFiles;
      const QString suffix = "pro";
      findFiles(dir, matchingFiles, suffix);
      // display the files
      cout << "Found " << matchingFiles.length() << " files with extensions: " << suffix
           << Qt::endl;
      foreach (const QString match, matchingFiles)
         cout << match << Qt::endl;
   }

   return EXIT_SUCCESS;
}
