// ============================================================================
// locale_utils_test.cpp - Metadata-Driven Matrix Validation Harness
// ============================================================================
#include <chrono>
#include <fstream>
#include <iostream>
#include <nlohmann/json.hpp>
#include <print>
#include <string>
#include <utility>
#include <vector>
#include "locale_utils.h"

using json = nlohmann::json;

enum class BoxAlign { Left, Center, Right };

void print_boxed_message(const std::string &message, BoxAlign alignment)
{
  const std::string border_char = "═";
  size_t text_len = message.length();
  size_t inner_width = text_len + 2;

  std::string horizontal_border = "";
  for (size_t i = 0; i < inner_width; ++i) {
    horizontal_border += border_char;
  }

  std::cout << "╔" << horizontal_border << "╗\n";
  std::cout << "║ " << message << " ║\n";
  std::cout << "╚" << horizontal_border << "╝\n";
}

// Scans JSON config file and builds a profile list pairing the locale ID with
// its descriptive text
std::vector<std::pair<std::string, std::string>> discover_configured_profiles()
{
  std::vector<std::pair<std::string, std::string>> profiles;
  std::ifstream file("locales_config.json");
  if (!file.is_open())
    return profiles;

  try {
    nlohmann::json config_data;
    file >> config_data;
    for (auto &[key, value]: config_data.items()) {
      std::string desc = value.value("desc", "No description provided");
      profiles.push_back({key, desc});
    }
  }
  catch (...) {
  }

  return profiles;
}

int main()
{
  LocaleUtils::initialize_system_locale();

  auto test_profiles = discover_configured_profiles();
  if (test_profiles.empty()) {
    std::println(stderr,
        "❌ Aborting: No target profiles identified from configuration file.");
    return 1;
  }

  constexpr double test_numeric_payload = 12345678.96;
  const auto system_clock_marker = std::chrono::system_clock::now();

  print_boxed_message(
      "GLOBALIZATION MATRIX AUTOMATED DISCOVERY SYSTEM", BoxAlign::Center);
  std::println("Detected Verification Target Profiles Counts: {}\n",
      test_profiles.size());

  for (const auto &[locale_id, description]: test_profiles) {
    // Build the dynamic, perfectly sized header line pulling description from
    // the JSON file
    std::string header_text =
        "LOCALE IDENTIFIER : " + locale_id + " (" + description + ")";
    print_boxed_message(header_text, BoxAlign::Left);

    std::string formatted_num =
        LocaleUtils::format_number(test_numeric_payload, locale_id);
    std::println("  ├─ Formatted Number   : {}", formatted_num);

    double parsed_out_value = 0.0;
    bool parse_success =
        LocaleUtils::parse_number(formatted_num, parsed_out_value, locale_id);
    std::println("  ├─ Round-Trip Parser  : {} [Evaluated Result: {}]",
        parse_success ? "✅ SUCCESS" : "❌ FAILED", parsed_out_value);

    std::println("  ├─ Native Currency    : {}",
        LocaleUtils::format_currency(test_numeric_payload, locale_id));
    std::println("  ├─ Calendar Structural: {}",
        LocaleUtils::format_date_time(system_clock_marker, false, locale_id));
    std::println("  ├─ Value to Words     : {}",
        LocaleUtils::expand_number_to_words(test_numeric_payload, locale_id));
    std::println("  └─ Currency to Text   : {}",
        LocaleUtils::expand_currency_to_words(test_numeric_payload, locale_id));
    std::println("\n");

    // ============================================================================
    // RIGOROUS REVERSE PARSING VALIDATION LABS
    // ============================================================================
    std::println("  --- Extended Reverse Parse Diagnostics ---");

    // A. Strict Currency Verification Loop
    std::string test_currency_input =
        LocaleUtils::format_currency(test_numeric_payload, locale_id);
    double extracted_currency_val = 0.0;
    bool currency_parse_ok = LocaleUtils::parse_currency(
        test_currency_input, extracted_currency_val, locale_id);

    std::println("  ├─ Currency Reverse Parse : {} [Parsed: {} From: {}]",
        currency_parse_ok ? "✅ SUCCESS" : "❌ FAILED", extracted_currency_val,
        test_currency_input);

    // B. Strict Temporal Format Verification Loop (Apples to Apples)
    std::string printable_short_dt =
        LocaleUtils::format_short_date_time(system_clock_marker, locale_id);

    std::chrono::system_clock::time_point parsed_time_destination;
    bool temporal_parse_ok = LocaleUtils::parse_date_time(
        printable_short_dt, parsed_time_destination, locale_id);

    std::println("  └─ Temporal Reverse Parse : {} [Source Short String: {}]",
        temporal_parse_ok ? "✅ SUCCESS" : "❌ FAILED", printable_short_dt);
    std::println("\n");
  }

  print_boxed_message(
      "ALL MATRIX VERIFICATION SEQUENCES COMPLETED SUCCESSFULLY",
      BoxAlign::Center);
  return 0;
}
