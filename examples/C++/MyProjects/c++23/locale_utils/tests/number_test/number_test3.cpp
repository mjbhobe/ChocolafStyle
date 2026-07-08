// =========================================================================
// number_test3.cpp - round-trip tests for LocaleUtils::format_number() and
//   LocaleUtils::parse_number() across multiple locales
//
// Build: see CMakeLists.txt in this folder
//
// Author: Manish Bhobe
// My experiments with C/C++, STL and Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// =========================================================================

#include <cmath>
#include <print>
#include <vector>
#include "locale_utils.h"

namespace {

  bool nearly_equal(double a, double b, double epsilon = 1e-6)
  {
    return std::fabs(a - b) < epsilon;
  }

} // namespace

int main()
{
  // use the user's locale settings
  LocaleUtils::initialize_system_locale();

  constexpr double large_value = 34573892785.34;
  int failures = 0;

  std::println("--- Round-trip: format_number() -> parse_number() ---");
  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN"}) {
    std::string formatted = LocaleUtils::format_number(large_value, locale_id);

    double parsed_value{};
    bool ok = LocaleUtils::parse_number(formatted, parsed_value, locale_id);
    bool round_trip_ok = ok && nearly_equal(parsed_value, large_value);

    std::println("[{}] formatted = \"{}\", parsed = {}, round-trip {}",
        locale_id, formatted, parsed_value, round_trip_ok ? "OK" : "FAILED");

    if (!round_trip_ok)
      ++failures;
  }

  std::println("\nSimulated I/O for en_IN locale...");
  // let's pretend user entered these values on command line when prompted
  // and we read that in as a string with std::getline()
  // for en_IN locale, the first 2 should parse ok - rest should fail
  std::vector<std::string> num_values{
    "34,57,38,92,785.34", // ok
    "34573892785.34",     // ok
    "34,573,892,785.34",  // fail
    "34 573 892 785,34"   // fail
  };
  const std::string locale_id = "en_IN";
  for (const auto val : num_values) {
    double parsed_value{};

    bool ok = LocaleUtils::parse_number(val, parsed_value, locale_id);    
    if (ok) {
      std::println("Number entered as {} parsed successfully as {}", val, parsed_value);
    } else {
      std::println("Error parsing {} using locale_id {}", val, locale_id);
    }
  }


  std::println("\n--- Rejecting garbage input ---");
  double bogus_value{};
  bool bogus_ok =
      LocaleUtils::parse_number("not-a-number", bogus_value, "en_US");
  std::println("parse_number(\"not-a-number\") -> {} ({})", bogus_ok,
      bogus_ok ? "unexpectedly succeeded" : "correctly rejected");

  if (bogus_ok)
    ++failures;

  std::println("\n{} check(s) failed.", failures);
  return failures == 0 ? 0 : 1;
}
