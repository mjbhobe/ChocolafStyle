// =========================================================================
// number_test4.cpp - number to text spellout tests for
//      LocaleUtils::spellout_number() across multiple locales
//
// Build: see CMakeLists.txt in this folder
//
// Author: Manish Bhobe
// My experiments with C/C++, STL and Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// =========================================================================
#include <print>
#include "locale_utils.h"

namespace locu = LocaleUtils;

int main()
{
  locu::initialize_system_locale();

  constexpr double large_value = 34573892785.34;

  for (const auto &locale_id: {"en_US", "fr_FR", "ru_RU", "en_IN"}) {
    std::println("--- {} ---", locale_id);
    std::println(
        "Display : {}", locu::format_number(large_value, locale_id));
    std::println("Spelled : {}",
        locu::expand_number_to_words(large_value, locale_id));

    // Round-trip: parse the display string straight back into a double.
    double parsed_value{};
    std::string displayed = locu::format_number(large_value, locale_id);
    bool ok = locu::parse_number(displayed, parsed_value, locale_id);
    std::println(
        "Parsed  : {} (round-trip {})", parsed_value, ok ? "OK" : "FAILED");
  }
}
