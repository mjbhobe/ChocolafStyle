// ---------------------------------------------------------------------
// main.cpp - thorough test of readFloatType() and parseFloatType()
// (declared in common_funcs.h) across both FloatType types (float,
// double) and three locales: the default QLocale::c(), en_IN (India,
// which groups digits as "12,34,567"), and de_DE (Germany, which uses
// '.' as the group separator and ',' as the DECIMAL POINT - the key
// difference from the integer test, since float/double parsing also
// has to get the decimal separator right, not just digit grouping).
//
// readFloatType() normally prompts and reads a line from a live
// QTextStream (stdin). To keep this test non-interactive, each input
// line is fed through a QTextStream constructed over an in-memory
// QString buffer instead of stdin - readLine() behaves identically
// either way.
//
// Floating-point results are compared with a relative-epsilon check
// rather than ==, since a parsed value and a hand-written literal for
// the same decimal text are not guaranteed to be bit-identical for
// every possible value, even though both round to the nearest double
// via a correctly-rounded conversion.
//
// @author: Manish Bhobe
// My experiments with C++/STL and Qt Framework
// Code is shared for learning purposes only!
// ---------------------------------------------------------------------
#include <QCoreApplication>
#include <QLocale>
#include <QString>
#include <QTextStream>

#include <algorithm>
#include <cmath>
#include <limits>
#include <utility>

#include "common_funcs.h"

#ifdef USING_QT6
static QTextStream qcout(stdout, QIODeviceBase::WriteOnly);
#else
static QTextStream qcout(stdout, QIODevice::WriteOnly);
#endif

static int totalTests  = 0;
static int passedTests = 0;

// builds a QTextStream over an in-memory line of text, so readFloatType()
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

// relative-epsilon comparison, since a parsed float/double and a hand-typed
// literal for the same decimal text are not guaranteed bit-identical
template <FloatType T>
static bool approxEqual(T a, T b)
{
  const T scale = std::max<T>(T(1), std::max(std::abs(a), std::abs(b)));
  return std::abs(a - b) <= scale * std::numeric_limits<T>::epsilon() * T(100);
}

template <FloatType T>
static void testRead(const QString& typeName, const QString& localeName, const QLocale& locale,
                      const QString& inputLine, T expected)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readFloatType(in, value, "", locale);

  ++totalTests;
  bool pass = ok && approxEqual(value, expected);
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName
        << " | input=\"" << inputLine << "\" | ";
  if (ok)
    qcout << "value=" << value;
  else
    qcout << "value=<parse failed>";
  qcout << " | expected=" << expected << Qt::endl;
}

template <FloatType T>
static void testParse(const QString& typeName, const QString& localeName, const QLocale& locale,
                       const QString& inputStr, T expected)
{
  T value{};
  bool ok = parseFloatType(inputStr, value, locale);

  ++totalTests;
  bool pass = ok && approxEqual(value, expected);
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName
        << " | input=\"" << inputStr << "\" | ";
  if (ok)
    qcout << "value=" << value;
  else
    qcout << "value=<parse failed>";
  qcout << " | expected=" << expected << Qt::endl;
}

template <FloatType T>
static void testFailRead(const QString& typeName, const QString& localeName,
                          const QLocale& locale, const QString& inputLine, const QString& reason)
{
  QString buffer;
  QTextStream in = makeLineStream(buffer, inputLine);

  T value{};
  bool ok = readFloatType(in, value, "", locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | read  | " << localeName
        << " | input=\"" << inputLine << "\" | expected=<" << reason << ">" << Qt::endl;
}

template <FloatType T>
static void testFailParse(const QString& typeName, const QString& localeName,
                           const QLocale& locale, const QString& inputStr, const QString& reason)
{
  T value{};
  bool ok = parseFloatType(inputStr, value, locale);

  ++totalTests;
  bool pass = !ok;
  if (pass)
    ++passedTests;

  qcout << (pass ? "[PASS] " : "[FAIL] ") << typeName << " | parse | " << localeName
        << " | input=\"" << inputStr << "\" | expected=<" << reason << ">" << Qt::endl;
}

// runs both testFailRead() and testFailParse() for T with a single input/reason
template <FloatType T>
static void testFailBoth(const QString& typeName, const QString& localeName,
                          const QLocale& locale, const QString& inputStr, const QString& reason)
{
  testFailRead<T>(typeName, localeName, locale, inputStr, reason);
  testFailParse<T>(typeName, localeName, locale, inputStr, reason);
}

// runs both testRead() and testParse() for T across default/India/Germany
// locales, given the matching (default, India-grouped, Germany-grouped)
// input strings for the same expected value
template <FloatType T>
static void testAllLocales(const QString& typeName, const QLocale& cLocale,
                            const QLocale& inLocale, const QLocale& deLocale,
                            const QString& defaultInput, const QString& indiaInput,
                            const QString& germanyInput, T expected)
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

  const QLocale cLocale  = QLocale::c();
  const QLocale inLocale(QLocale::English, QLocale::India);
  const QLocale deLocale(QLocale::German, QLocale::Germany);

  qcout << "===== readFloatType()/parseFloatType() - all FloatType types, "
           "all locales =====" << Qt::endl;

  // float: 1234.5 (.5 is exactly representable in binary, so no rounding
  // ambiguity). Indian grouping of the integer part "1234" -> "1,234"
  // (same as western grouping for a 4-digit number). Germany swaps roles:
  // '.' groups digits, ',' is the decimal point -> "1.234,5"
  testAllLocales<float>("float", cLocale, inLocale, deLocale, "1234.5", "1,234.5", "1.234,5",
                         1234.5f);

  // double: 1234567.5 -> Indian grouping "12,34,567.5", German "1.234.567,5"
  testAllLocales<double>("double", cLocale, inLocale, deLocale, "1234567.5", "12,34,567.5",
                          "1.234.567,5", 1234567.5);

  qcout << Qt::endl << "===== negative values (double, representative) =====" << Qt::endl;
  testRead<double>("double", "default (C)", cLocale, "-1234567.5", -1234567.5);
  testRead<double>("double", "India (en_IN)", inLocale, "-12,34,567.5", -1234567.5);
  testRead<double>("double", "Germany (de_DE)", deLocale, "-1.234.567,5", -1234567.5);
  testParse<double>("double", "default (C)", cLocale, "-1234567.5", -1234567.5);
  testParse<double>("double", "India (en_IN)", inLocale, "-12,34,567.5", -1234567.5);
  testParse<double>("double", "Germany (de_DE)", deLocale, "-1.234.567,5", -1234567.5);

  qcout << Qt::endl << "===== scientific notation (double, default locale) =====" << Qt::endl;
  testRead<double>("double", "default (C)", cLocale, "1.5e10", 1.5e10);
  testParse<double>("double", "default (C)", cLocale, "1.5e10", 1.5e10);

  // ---- failure-path checks, run across ALL THREE locales -------------------
  // every case below was verified empirically against QLocale before being
  // written here (see PR discussion) - these are not assumptions.
  qcout << Qt::endl << "===== failure-path checks: garbage / trailing garbage / empty "
                        "(double, all locales) =====" << Qt::endl;
  for (const auto& [localeName, locale] :
       {std::pair{QString("default (C)"), cLocale}, std::pair{QString("India (en_IN)"), inLocale},
        std::pair{QString("Germany (de_DE)"), deLocale}}) {
    testFailBoth<double>("double", localeName, locale, "not-a-number", "garbage input");
    testFailBoth<double>("double", localeName, locale, "3.14abc", "trailing garbage");
    testFailBoth<double>("double", localeName, locale, "", "empty input");
  }

  qcout << Qt::endl << "===== failure-path checks: out-of-range "
                        "(float, all locales) =====" << Qt::endl;
  for (const auto& [localeName, locale] :
       {std::pair{QString("default (C)"), cLocale}, std::pair{QString("India (en_IN)"), inLocale},
        std::pair{QString("Germany (de_DE)"), deLocale}}) {
    // FLT_MAX is ~3.4e38, so 1e400 is always out of range regardless of locale
    testFailBoth<float>("float", localeName, locale, "1e400", "range overflow");
  }

  qcout << Qt::endl << "===== failure-path checks: cross-locale format mismatches "
                        "(double) =====" << Qt::endl;
  // a value formatted for one locale's decimal point/grouping convention
  // must be rejected by a DIFFERENT locale - this is what actually proves
  // the locale parameter changes behaviour, rather than just being
  // accepted/ignored everywhere
  testFailBoth<double>("double", "default (C)", cLocale, "1.234.567,5",
                        "Germany-formatted input rejected under C locale");
  testFailBoth<double>("double", "India (en_IN)", inLocale, "1.234.567,5",
                        "Germany-formatted input rejected under India locale");
  testFailBoth<double>("double", "Germany (de_DE)", deLocale, "12,34,567.5",
                        "India/C-formatted input rejected under Germany locale");

  qcout << Qt::endl << "===== Summary: " << passedTests << "/" << totalTests << " passed ====="
        << Qt::endl;

  return (passedTests == totalTests) ? EXIT_SUCCESS : EXIT_FAILURE;
}
