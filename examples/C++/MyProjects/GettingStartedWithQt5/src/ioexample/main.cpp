// ---------------------------------------------------------------------
// main.cpp - demonstrates reading standard data types from QTextStream,
// plus QDate/QTime (which have no operator>> support and must be parsed
// from a QString token instead)
//
// NOTE: we deliberately never use operator>> here. Mixing operator>>
// (which leaves the trailing '\n' in the stream) with readLine() (which
// immediately consumes that leftover '\n' as an empty line) is the same
// classic bug as mixing std::qcin >> with std::getline. The fix is to
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

#include <ctime>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <fstream>

static QTextStream qcout(stdout, QIODevice::WriteOnly);
static QTextStream qcerr(stderr, QIODevice::WriteOnly);
static QTextStream qcin(stdin, QIODevice::ReadOnly);

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);

  // --- QChar -------------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a single character: " << Qt::flush;
  QString chLine = qcin.readLine().trimmed();
  QChar ch = chLine.isEmpty() ? QChar() : chLine.at(0);
  qcout << "  You entered: " << ch << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a single character: " << std::flush;
  std::string chLineStl;
  std::getline(std::cin, chLineStl);
  std::istringstream chStreamStl(chLineStl);
  char chStl = '\0';
  chStreamStl >> chStl;
  std::cout << "  You entered: " << chStl << std::endl;

  // --- QString -------------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a string: " << Qt::flush;
  QString text = qcin.readLine();
  qcout << "  You entered: " << text << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a string: " << std::flush;
  std::string textStl;
  std::getline(std::cin, textStl);
  std::cout << "  You entered: " << textStl << std::endl;

  // --- int ---------------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter an integer: " << Qt::flush;
  bool ok{false};
  int intVal = qcin.readLine().trimmed().toInt(&ok);
  if (ok)
    qcout << "  You entered: " << intVal << Qt::endl;
  else
    qcerr << "  Error: not a valid integer!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter an integer: " << std::flush;
  std::string intLineStl;
  std::getline(std::cin, intLineStl);
  std::istringstream intStreamStl(intLineStl);
  int intValStl{};
  bool okStl = static_cast<bool>(intStreamStl >> intValStl) && (intStreamStl >> std::ws).eof();
  if (okStl)
    std::cout << "  You entered: " << intValStl << std::endl;
  else
    std::cerr << "  Error: not a valid integer!" << std::endl;

  // --- unsigned long -------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter an unsigned long: " << Qt::flush;
  unsigned long ulongVal = qcin.readLine().trimmed().toULong(&ok);
  if (ok)
    qcout << "  You entered: " << ulongVal << Qt::endl;
  else
    qcerr << "  Error: not a valid unsigned long!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter an unsigned long: " << std::flush;
  std::string ulongLineStl;
  std::getline(std::cin, ulongLineStl);
  std::istringstream ulongStreamStl(ulongLineStl);
  unsigned long ulongValStl{};
  bool ulongOkStl = static_cast<bool>(ulongStreamStl >> ulongValStl) && (ulongStreamStl >>
    std::ws).eof();
  if (ulongOkStl)
    std::cout << "  You entered: " << ulongValStl << std::endl;
  else
    std::cerr << "  Error: not a valid unsigned long!" << std::endl;

  // --- qlonglong (qint64) --------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a large integer (qint64): " << Qt::flush;
  qlonglong llVal = qcin.readLine().trimmed().toLongLong(&ok);
  if (ok)
    qcout << "  You entered: " << llVal << Qt::endl;
  else
    qcerr << "  Error: not a valid qint64!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a large integer (long long): " << std::flush;
  std::string llLineStl;
  std::getline(std::cin, llLineStl);
  std::istringstream llStreamStl(llLineStl);
  long long llValStl{};
  bool llOkStl = static_cast<bool>(llStreamStl >> llValStl) && (llStreamStl >> std::ws).eof();
  if (llOkStl)
    std::cout << "  You entered: " << llValStl << std::endl;
  else
    std::cerr << "  Error: not a valid long long!" << std::endl;

  // --- float ---------------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a float: " << Qt::flush;
  float floatVal = qcin.readLine().trimmed().toFloat(&ok);
  if (ok)
    qcout << "  You entered: " << floatVal << Qt::endl;
  else
    qcerr << "  Error: not a valid float!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a float: " << std::flush;
  std::string floatLineStl;
  std::getline(std::cin, floatLineStl);
  std::istringstream floatStreamStl(floatLineStl);
  float floatValStl{};
  bool floatOkStl = static_cast<bool>(floatStreamStl >> floatValStl) && (floatStreamStl >>
    std::ws).eof();
  if (floatOkStl)
    std::cout << "  You entered: " << floatValStl << std::endl;
  else
    std::cerr << "  Error: not a valid float!" << std::endl;

  // --- double ----------------------------------------------------------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a double: " << Qt::flush;
  double doubleVal = qcin.readLine().trimmed().toDouble(&ok);
  if (ok)
    qcout << "  You entered: " << doubleVal << Qt::endl;
  else
    qcerr << "  Error: not a valid double!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a double: " << std::flush;
  std::string doubleLineStl;
  std::getline(std::cin, doubleLineStl);
  std::istringstream doubleStreamStl(doubleLineStl);
  double doubleValStl{};
  bool doubleOkStl = static_cast<bool>(doubleStreamStl >> doubleValStl) && (doubleStreamStl >>
    std::ws).eof();
  if (doubleOkStl)
    std::cout << "  You entered: " << doubleValStl << std::endl;
  else
    std::cerr << "  Error: not a valid double!" << std::endl;

  // --- QDate (no operator>> exists - read as QString, then parse) ------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a date (dd-MM-yyyy): " << Qt::flush;
  QString dateStr = qcin.readLine().trimmed();
  QDate date = QDate::fromString(dateStr, "dd-MM-yyyy");
  if (date.isValid())
    qcout << "  You entered: " << date.toString("dd-MMM-yyyy") << Qt::endl;
  else
    qcerr << "  Error: " << dateStr << " is not a valid date!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a date (dd-MM-yyyy): " << std::flush;
  std::string dateLineStl;
  std::getline(std::cin, dateLineStl);
  std::tm tmDateStl{};
  std::istringstream dateStreamStl(dateLineStl);
  dateStreamStl >> std::get_time(&tmDateStl, "%d-%m-%Y");
  bool dateOkStl = !dateStreamStl.fail() && (dateStreamStl >> std::ws).eof();
  if (dateOkStl)
    std::cout << "  You entered: " << std::put_time(&tmDateStl, "%d-%b-%Y") << std::endl;
  else
    std::cerr << "  Error: " << dateLineStl << " is not a valid date!" << std::endl;

  // --- QTime (no operator>> exists - read as QString, then parse) ------
  qcout << "Qt version" << Qt::endl;
  qcout << "Enter a time (HH:mm:ss): " << Qt::flush;
  QString timeStr = qcin.readLine().trimmed();
  QTime time = QTime::fromString(timeStr, "HH:mm:ss");
  if (time.isValid())
    qcout << "  You entered: " << time.toString("hh:mm:ss AP") << Qt::endl;
  else
    qcerr << "  Error: " << timeStr << " is not a valid time!" << Qt::endl;

  // Now the same code with STL
  std::cout << "STL version" << std::endl;
  std::cout << "Enter a time (HH:mm:ss): " << std::flush;
  std::string timeLineStl;
  std::getline(std::cin, timeLineStl);
  std::tm tmTimeStl{};
  std::istringstream timeStreamStl(timeLineStl);
  timeStreamStl >> std::get_time(&tmTimeStl, "%H:%M:%S");
  bool timeOkStl = !timeStreamStl.fail() && (timeStreamStl >> std::ws).eof();
  if (timeOkStl)
    std::cout << "  You entered: " << std::put_time(&tmTimeStl, "%I:%M:%S %p") << std::endl;
  else
    std::cerr << "  Error: " << timeLineStl << " is not a valid time!" << std::endl;

  // some code with std::string & QString -------------------------------

  std::cout << "Working with std::string ---------" << std::endl;
  std::string ss1{"This "}, ss2{"is a "}, ss3{"std::string"};
  std::cout << ss1 << ss2 << ss3 << std::endl;
  ss1 += ss2;
  std::cout << ss1 << std::endl;
  std::string ss4 = ss1 + ss3;
  std::cout << ss4 << std::endl;

  qcout << "Now similar code with QString ---------" << Qt::endl;
  QString s1{"This "}, s2{"is a "}, s3{"QString!"};
  qcout << s1 << s2 << s3 << Qt::endl;
  s1 += s2;
  qcout << s1 << Qt::endl;
  QString s4 = s1 + s3;
  qcout << "s4 = " << s4 << Qt::endl;
  std::cout << "------------------------------------\n" << std::endl;

  // displaying numbers in various styles --------------------------------

  // integers
  int num1{1234};
  qcout << "Dec: " << num1 << " Oct: " << Qt::oct << num1 << " Hex: " << Qt::hex << num1 <<
    Qt::endl;
  // floats
  double dub{1234.5678};
  qcout << "Double: " << dub << " Force sign: " << Qt::forcesign << dub << " Force point: " <<
    Qt::forcepoint << dub << Qt::endl;
  // reset the iostream
  qcout.reset();
  qcout << "Double: " << dub << " Fixed: " << Qt::fixed << dub << " Scientiic: " <<
    Qt::scientific << dub << " No Force sign: " << Qt::noforcesign << dub << Qt::endl;


  return EXIT_SUCCESS;
}
