// streams.cc - illustrating Qt streams
#include <cstdio>
#include <QString>
#include <QDebug>
#include <QTextStream>
#include <QFile>

QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);


int main(void) {
   QString str, newStr;
   QTextStream strbuf(&str);

   int lucky{7};
   float pi{3.1415f};
   double e{2.71828};
   const auto SPACE{' '};

   cout << "An in-memory stream" << Qt::endl;
   strbuf << "luckynumber: " << lucky << Qt::endl
      << "pi: " << pi << Qt::endl
      << "e: " << e << Qt::endl;
   // when writing to strbuf, you are actually writing to underlying QString
   cout << "Contents of in-memory stream" << Qt::endl;
   cout << str;

   // write stream to file
   cout << "Writing in-mem stream to file" << Qt::endl;
   const auto DATA_FILE = "mydata2.dat";
   QFile data(DATA_FILE);
   if (data.open(QIODeviceBase::WriteOnly)) {
      QTextStream out(&data);
      out << str;
      data.close();
   }
   else 
      cerr << "FATAL: unable to open file " << DATA_FILE << " for writing!" << Qt::endl;

   // read from file
   cout << "Reading values from file" << Qt::endl;
   QFile data2(DATA_FILE);
   if (data2.open(QIODevice::ReadOnly)) {
      QTextStream in(&data2);
      QString newstr;

      // read first line with int
      int lucky2;
      in >> newstr >> lucky2;
      if (lucky != lucky2)
         cerr << "ERROR reading file " << newstr << SPACE << lucky2 << Qt::endl;
      else 
         cout << "Read -> " << newstr << SPACE << lucky2 << Qt::endl;

      // read second line with pi
      float pi2;
      in >> newstr >> pi2;
      if (pi != pi2)
         cerr << "ERROR reading file " << newstr << SPACE << pi2 << Qt::endl;
      else 
         cout << "Read -> " << newstr << SPACE << pi2 << Qt::endl;

      // read 3rd line with e
      double e2; 
      in >> newstr >> e2;
      if (e != e2)
         cerr << "ERROR reading file " << newstr << SPACE << e2 << Qt::endl;
      else 
         cout << "Read -> " << newstr << SPACE << e2 << Qt::endl;

      data2.close();
   }
   else 
      cerr << "FATAL: unable to open file " << DATA_FILE << " for reading!" << Qt::endl;

   // read contents line by line from file
   cout << "Read file contents line by line..." << Qt::endl;
   if (data.open(QIODevice::ReadOnly)) {
      QTextStream in(&data);
      QString newstr;

      while (! in.atEnd()) {
         newstr = in.readLine();
         cout << newstr << Qt::endl;
      }
      data.close();
   }

   return 0;
}



