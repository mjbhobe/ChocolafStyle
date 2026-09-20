// main.cpp - demonstrates reading standard data types from QTextStream,
// plus QDate/QTime (which have no operator>> support and must be parsed
// from a QString token instead)
//
// NOTE: we deliberately never use operator>> here. Mixing operator>>
// (which leaves the trailing '\n' in the stream) with readLine() (which
// immediately consumes that leftover '\n' as an empty line) is the same
// classic bug as mixing std::cin >> with std::getline. The fix is to
// pick ONE style consistently: read a full line every time, then parse
// it into whatever type you need. That way no read ever leaves anything
// behind for the next one.
//
// @author: Manish Bhobe
// My experiments with C++/STL and Qt Framework
// Code is shared for learning purposes only!
// ---------------------------------------------------------------------
#include <QCoreApplication>
#include <QDate>
#include <QIODevice>
#include <QString>
#include <QTextStream>
#include <QTime>

// DO NOT include <iostream>
static QTextStream cout(stdout, QIODevice::WriteOnly);
static QTextStream cerr(stderr, QIODevice::WriteOnly);
static QTextStream cin(stdin, QIODevice::ReadOnly);

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);

  // --- QChar -------------------------------------------------------------
  cout << "Enter a single character: " << Qt::flush;
  QString chLine = cin.readLine().trimmed();
  QChar ch       = chLine.isEmpty() ? QChar() : chLine.at(0);
  cout << "  You entered: " << ch << Qt::endl;

  // --- QString -------------------------------------------------------------
  cout << "Enter a string: " << Qt::flush;
  QString text = cin.readLine();
  cout << "  You entered: " << text << Qt::endl;

  // --- int ---------------------------------------------------------------
  cout << "Enter an integer: " << Qt::flush;
  bool ok{false};
  int intVal = cin.readLine().trimmed().toInt(&ok);
  if (ok)
    cout << "  You entered: " << intVal << Qt::endl;
  else
    cerr << "  Error: not a valid integer!" << Qt::endl;

  // --- unsigned long -------------------------------------------------------
  cout << "Enter an unsigned long: " << Qt::flush;
  unsigned long ulongVal = cin.readLine().trimmed().toULong(&ok);
  if (ok)
    cout << "  You entered: " << ulongVal << Qt::endl;
  else
    cerr << "  Error: not a valid unsigned long!" << Qt::endl;

  // --- qlonglong (qint64) --------------------------------------------------
  cout << "Enter a large integer (qint64): " << Qt::flush;
  qlonglong llVal = cin.readLine().trimmed().toLongLong(&ok);
  if (ok)
    cout << "  You entered: " << llVal << Qt::endl;
  else
    cerr << "  Error: not a valid qint64!" << Qt::endl;

  // --- float ---------------------------------------------------------------
  cout << "Enter a float: " << Qt::flush;
  float floatVal = cin.readLine().trimmed().toFloat(&ok);
  if (ok)
    cout << "  You entered: " << floatVal << Qt::endl;
  else
    cerr << "  Error: not a valid float!" << Qt::endl;

  // --- double ----------------------------------------------------------
  cout << "Enter a double: " << Qt::flush;
  double doubleVal = cin.readLine().trimmed().toDouble(&ok);
  if (ok)
    cout << "  You entered: " << doubleVal << Qt::endl;
  else
    cerr << "  Error: not a valid double!" << Qt::endl;

  // --- QDate (no operator>> exists - read as QString, then parse) ------
  cout << "Enter a date (dd-MM-yyyy): " << Qt::flush;
  QString dateStr = cin.readLine().trimmed();
  QDate date      = QDate::fromString(dateStr, "dd-MM-yyyy");
  if (date.isValid())
    cout << "  You entered: " << date.toString("dd-MMM-yyyy") << Qt::endl;
  else
    cerr << "  Error: " << dateStr << " is not a valid date!" << Qt::endl;

  // --- QTime (no operator>> exists - read as QString, then parse) ------
  cout << "Enter a time (HH:mm:ss): " << Qt::flush;
  QString timeStr = cin.readLine().trimmed();
  QTime time      = QTime::fromString(timeStr, "HH:mm:ss");
  if (time.isValid())
    cout << "  You entered: " << time.toString("hh:mm:ss AP") << Qt::endl;
  else
    cerr << "  Error: " << timeStr << " is not a valid time!" << Qt::endl;

  // some code with QString -----------------------------------------------
  QString s1{"This "}, s2{"is a "}, s3{"QString!"};
  cout << s1 << s2 << s3 << Qt::endl;
  s1 += s2;
  cout << s1 << Qt::endl;
  QString s4 = s1 + s3;
  cout << "s4 = " << s4 << Qt::endl;

  return EXIT_SUCCESS;
}
