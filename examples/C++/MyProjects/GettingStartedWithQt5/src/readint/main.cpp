// ---------------------------------------------------------------------
// main.cpp - thorough test of readIntegerType() and parseIntegerType()
// (declared in common_funcs.h) across every IntegerType (short, unsigned
// short, int, unsigned int, long, unsigned long, long long, unsigned long
// long) and three locales: the default QLocale::c(), en_IN (India, which
// groups digits as "12,34,567"), and de_DE (Germany, which uses '.' as
// the group separator and ',' as the decimal point).
//
// readIntegerType() normally prompts and reads a line from a live
// QTextStream (stdin). To keep this test non-interactive, each input line
// is fed through a QTextStream constructed over an in-memory QString
// buffer instead of stdin - readLine() behaves identically either way.
//
// @author: Manish Bhobe
// My experiments with C++/STL and Qt Framework
// Code is shared for learning purposes only!
// ---------------------------------------------------------------------
#include <QCoreApplication>
#include <QLocale>
#include <QString>
#include <QTextStream>

#include <utility>

#include "common_funcs.h"

// ---- compile-time verification of the IntegerType concept fix ----
// signed char / unsigned char (qint8/quint8) satisfy std::integral but have
// no dispatch branch in readIntegerType()'s/parseIntegerType()'s
// if constexpr chains - IntegerType must therefore exclude them. If either
// assert below ever fires, the concept has regressed and
// readIntegerType<signed char> would go back to silently, always returning
// false at runtime instead of failing to compile at the call site.
static_assert(!IntegerType<signed char>, "IntegerType must exclude signed char (qint8)");
static_assert(!IntegerType<unsigned char>, "IntegerType must exclude unsigned char (quint8)");
// sanity check: the fix above must not have become overly broad and
// accidentally excluded a real integer type too
static_assert(IntegerType<short> && IntegerType<unsigned short> && IntegerType<int> &&
                  IntegerType<unsigned int> && IntegerType<long> && IntegerType<unsigned long> &&
                  IntegerType<long long> && IntegerType<unsigned long long>,
              "IntegerType must still accept every real integer type");

#ifdef USING_QT6
static QTextStream qcout(stdout, QIODeviceBase::WriteOnly);
#else
static QTextStream qcout(stdout, QIODevice::WriteOnly);
#endif

static int totalTests = 0;
static int passedTests = 0;

// builds a QTextStream over an in-memory line of text, so readIntegerType()
// can be exercised without real stdin input
#ifdef USING_QT6
static QTextStream makeLineStream(QString& buffer, const QString& line)
{
  buffer = line + "\n";
  return QTextStream(&buffer, QIODeviceBase::ReadOnly);
}
#else
static QTextStream makeLineStream(QString& buffer, const QString& line)
{
  buffer = line + "\n";
  return QTextStream(&buffer, QIODevice::ReadOnly);
}
#endif

template <IntegerType T>
static void testRead(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputLine, T expected
)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readIntegerType(in, value, "", locale);

  ++totalTests;
  bool pass = ok && value == expected;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName <<
    " | input=\"" << inputLine << "\" | ";
  if (ok)
    qcout << "value=" << value;
  else
    qcout << "value=<parse failed>";
  qcout << " | expected=" << expected << Qt::endl;
}

template <IntegerType T>
static void testParse(
  const QString& typeName, const QString& localeName, const QLocale& locale,
  const QString& inputStr, T expected
)
{
  T value{};
  bool ok = parseIntegerType(inputStr, value, locale);

  ++totalTests;
  bool pass = ok && value == expected;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName <<
    " | input=\"" << inputStr << "\" | ";
  if (ok)
    qcout << "value=" << value;
  else
    qcout << "value=<parse failed>";
  qcout << " | expected=" << expected << Qt::endl;
}

template <IntegerType T>
static void testFailRead(const QString& typeName, const QString& localeName,
                          const QLocale& locale, const QString& inputLine, const QString& reason)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readIntegerType(in, value, "", locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName
        << " | input=\"" << inputLine << "\" | expected=<" << reason << ">" << Qt::endl;
}

template <IntegerType T>
static void testFailParse(const QString& typeName, const QString& localeName,
                           const QLocale& locale, const QString& inputStr, const QString& reason)
{
  T value{};
  bool ok = parseIntegerType(inputStr, value, locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName
        << " | input=\"" << inputStr << "\" | expected=<" << reason << ">" << Qt::endl;
}

// runs both testFailRead() and testFailParse() for T with a single input/reason
template <IntegerType T>
static void testFailBoth(const QString& typeName, const QString& localeName,
                          const QLocale& locale, const QString& inputStr, const QString& reason)
{
  testFailRead<T>(typeName, localeName, locale, inputStr, reason);
  testFailParse<T>(typeName, localeName, locale, inputStr, reason);
}

// runs both testRead() and testParse() for T across default/India/Germany
// locales, given the matching (default, India-grouped, Germany-grouped)
// input strings for the same expected value
template <IntegerType T>
static void testAllLocales(
  const QString& typeName, const QLocale& cLocale, const QLocale& inLocale,
  const QLocale& deLocale, const QString& defaultInput, const QString& indiaInput,
  const QString& germanyInput, T expected
)
{
  testRead<T>(typeName, "default (C)", cLocale, defaultInput, expected);
  testRead<T>(typeName, "India (en_IN)", inLocale, indiaInput, expected);
  testRead<T>(typeName, "Germany (de_DE)", deLocale, germanyInput, expected);

  testParse<T>(typeName, "default (C)", cLocale, defaultInput, expected);
  testParse<T>(typeName, "India (en_IN)", inLocale, indiaInput, expected);
  testParse<T>(typeName, "Germany (de_DE)", deLocale, germanyInput, expected);
}

int main(int argc, char** argv)
{
  QCoreApplication app(argc, argv);

  const QLocale cLocale = QLocale::c();
  const QLocale inLocale(QLocale::English, QLocale::India);
  const QLocale deLocale(QLocale::German, QLocale::Germany);

  qcout << "===== readIntegerType()/parseIntegerType() - all IntegerType types, "
    "all locales =====" << Qt::endl;

  // short: 1234 (fits comfortably under SHRT_MAX == 32767)
  testAllLocales<short>("short", cLocale, inLocale, deLocale, "1234", "1,234", "1.234", 1234);

  // unsigned short: 54321 (fits under USHRT_MAX == 65535)
  testAllLocales<unsigned short>(
    "unsigned short", cLocale, inLocale, deLocale, "54321", "54,321", "54.321", 54321u
  );

  // int: 1234567 -> Indian grouping "12,34,567", western/German grouping "1.234.567"
  testAllLocales<int>(
    "int", cLocale, inLocale, deLocale, "1234567", "12,34,567", "1.234.567", 1234567
  );

  // unsigned int: same digits as int, reused
  testAllLocales<unsigned int>(
    "unsigned int", cLocale, inLocale, deLocale, "1234567", "12,34,567", "1.234.567", 1234567u
  );

  // long: same digits as int, reused
  testAllLocales<long>(
    "long", cLocale, inLocale, deLocale, "1234567", "12,34,567", "1.234.567", 1234567L
  );

  // unsigned long: same digits as int, reused
  testAllLocales<unsigned long>(
    "unsigned long", cLocale, inLocale, deLocale, "1234567", "12,34,567", "1.234.567",
    1234567UL
  );

  // long long (qint64): 1234567890 -> Indian grouping "1,23,45,67,890",
  // western/German grouping "1.234.567.890"
  testAllLocales<long long>(
    "long long", cLocale, inLocale, deLocale, "1234567890", "1,23,45,67,890", "1.234.567.890",
    1234567890LL
  );

  // unsigned long long (quint64): same digits as long long, reused
  testAllLocales<unsigned long long>(
    "unsigned long long", cLocale, inLocale, deLocale, "1234567890", "1,23,45,67,890",
    "1.234.567.890", 1234567890ULL
  );

  qcout << Qt::endl << "===== signed/negative values (int, representative) =====" << Qt::endl;
  testRead<int>("int", "default (C)", cLocale, "-1234567", -1234567);
  testRead<int>("int", "India (en_IN)", inLocale, "-12,34,567", -1234567);
  testParse<int>("int", "default (C)", cLocale, "-1234567", -1234567);
  testParse<int>("int", "India (en_IN)", inLocale, "-12,34,567", -1234567);

  // ---- failure-path checks, run across ALL THREE locales -------------------
  // every case below was verified empirically against QLocale before being
  // written here (see PR discussion) - these are not assumptions.
  qcout << Qt::endl << "===== failure-path checks: garbage / trailing garbage / empty "
                        "(int, all locales) =====" << Qt::endl;
  for (const auto& [localeName, locale] :
       {std::pair{QString("default (C)"), cLocale}, std::pair{QString("India (en_IN)"), inLocale},
        std::pair{QString("Germany (de_DE)"), deLocale}}) {
    testFailBoth<int>("int", localeName, locale, "not-a-number", "garbage input");
    testFailBoth<int>("int", localeName, locale, "42abc", "trailing garbage");
    testFailBoth<int>("int", localeName, locale, "", "empty input");
  }

  qcout << Qt::endl << "===== failure-path checks: out-of-range "
                        "(short, all locales) =====" << Qt::endl;
  for (const auto& [localeName, locale] :
       {std::pair{QString("default (C)"), cLocale}, std::pair{QString("India (en_IN)"), inLocale},
        std::pair{QString("Germany (de_DE)"), deLocale}}) {
    // SHRT_MAX is 32767, so 999999 is always out of range regardless of locale
    testFailBoth<short>("short", localeName, locale, "999999", "range overflow");
  }

  qcout << Qt::endl << "===== failure-path checks: cross-locale format mismatches "
                        "(int) =====" << Qt::endl;
  // a string grouped for one locale must be rejected by a DIFFERENT locale -
  // this is what actually proves the locale parameter changes behaviour,
  // rather than just being accepted/ignored everywhere
  testFailBoth<int>("int", "default (C)", cLocale, "12,34,567",
                     "India-grouped input rejected under C locale");
  testFailBoth<int>("int", "default (C)", cLocale, "1.234.567",
                     "Germany-grouped input rejected under C locale");
  testFailBoth<int>("int", "India (en_IN)", inLocale, "1.234.567",
                     "Germany-grouped input rejected under India locale");
  testFailBoth<int>("int", "Germany (de_DE)", deLocale, "12,34,567",
                     "India-grouped input rejected under Germany locale");

  qcout << Qt::endl << "===== Summary: " << passedTests << "/" << totalTests << " passed ====="
    << Qt::endl;

  return (passedTests == totalTests) ? EXIT_SUCCESS : EXIT_FAILURE;
}
