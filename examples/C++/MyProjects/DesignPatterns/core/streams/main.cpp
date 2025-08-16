#include <cstdio>
#include <cstdlib>
#include <QCoreApplication>
#include <QDate>
#include <QTextStream>

// NOTE: do not include <iostream>!
QTextStream cout(stdout, QIODeviceBase::WriteOnly);
QTextStream cerr(stderr, QIODeviceBase::WriteOnly);
QTextStream cin(stdin, QIODeviceBase::ReadOnly);

template<class T>
QTextStream &operator<<(QTextStream &ts, const QList<T> &lst)
{
   ts << "[";
   for (auto iter = lst.begin(); iter != lst.end() - 1; ++iter)
      ts << *iter << " ";
   ts << *(lst.end() - 1) << "]" << Qt::endl;
   return ts;
}

QTextStream &operator<<(QTextStream &ts, const QStringList &lst)
{
   ts << "[";
   for (auto iter = lst.begin(); iter != lst.end() - 1; ++iter)
      ts << *iter << " ";
   ts << *(lst.end() - 1) << "]" << Qt::endl;
   return ts;
}

struct student_rec {
   long id;
   QString name;
   float average;
   QDate birthday;

   friend QTextStream &operator<<(QTextStream &ts, const student_rec &rec)
   {
      ts << QString("%1 %2 %3 %4%")
               .arg(rec.id, 4)
               .arg(rec.name, 20)
               .arg(rec.birthday.toString("dd-MMM-yy"))
               .arg(rec.average, 6, 'f', 2)
         << Qt::endl;
      return ts;
   }
};

/**
 * @brief readDate - reads date in dd/mm/yyyy format from stdin
 * @param date (QDate) - return date read in this parameter
 * @param prompt - optional prompt to read date
 * @return true if date was ready correctly (dd/mm/yyyy format), else false
 */
bool readDate(QDate &date, const QString &prompt = "")
{
   bool ok = true;
   if (prompt != "")
      cout << prompt;

   fflush(stdin);
   QString val = cin.readLine();
   // dates will be read in dd/mm/yyyy format
   QStringList date_parts = val.split('/');
   int year = date_parts[2].toInt(&ok);
   if (!ok)
      return false;
   int month = date_parts[1].toInt(&ok);
   if (!ok)
      return false;
   int day = date_parts[0].toInt(&ok);
   if (!ok)
      return false;
   date = QDate(year, month, day);
   return true;
}

bool getStudentRec(student_rec &rec)
{
   // Tip: Always read a string from command line & convert
   // to desired data type (int, long, float etc.)
   QString val;
   bool ok;

   fflush(stdin);
   cout << "Roll no? " << Qt::flush;
   val = cin.readLine();
   rec.id = val.toInt(&ok);
   if (ok && rec.id < 0)
      return false;
   cout << "Name? " << Qt::flush;
   rec.name = cin.readLine();
   cout << "Average? " << Qt::flush;
   val = cin.readLine();
   rec.average = val.toFloat(&ok);
   if (!ok)
      return false;
   cout << "Birthday (dd/mm/yyyy)? " << Qt::flush;
   QDate birthday;
   if (!readDate(birthday))
      return false;
   rec.birthday = birthday;
   return true;
}

int main(int argc, char *argv[])
{
   QCoreApplication a(argc, argv);

   QString name{"Manish Bhobé"};
   cout << QString("Hello %1! Welcome to Qt %2").arg(name).arg(QT_VERSION_STR)
        << Qt::endl;
   QStringList favProgLanguages{"Python", "C++", "Java", "SQL"};
   cout << QString("These are a few of my favourite languages: ") << favProgLanguages
        << Qt::endl;

   QList<student_rec> recs{
      {10, "Manish Bhobé", 76.45f, QDate(1969, 6, 22)},
      {20, "Anupa Sardesai", 85.34f, QDate(1976, 1, 22)},
      {30, "Nupoor Bhobé", 98.45f, QDate(2007, 5, 8)},
   };

   student_rec rec{1, "", 0.0f, QDate()};
   while (getStudentRec(rec))
      recs.append(rec);
   cout << "Student report: " << Qt::endl;
   // just print out the whole list
   cout << recs;
   QDate today = QDate::currentDate();
   cout << "Today is " << today.toString("dd-MMM-yy") << Qt::endl;
   cout << recs[0].name << " is approx " << today.year() - recs[0].birthday.year()
        << " years old today" << Qt::endl;

   return EXIT_SUCCESS;
}
