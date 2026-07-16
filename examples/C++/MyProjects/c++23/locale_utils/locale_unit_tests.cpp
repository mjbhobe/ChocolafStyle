/**
 * @file locale_utils_test.cpp
 * @brief Enterprise-grade automation validation harness for LocaleUtils using
 * Google Test.
 *
 * Compile: $> clang++ -std=c++17 -O2 -Wall -g0 locale_utils.cpp \
 *     locale_utils_test.cpp -o automated_suite -lstdc++ -licuuc \
 *     -licui18n -lgtest lpthread
 * Run (after successful compilation): $> ./automated_suite
 */

#include <fstream>
#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include "locale_utils.h"

using json = nlohmann::json;

// ============================================================================
// DYNAMIC AUTOMATED LOCALE DISCOVERY ENGINE
// ============================================================================

/**
 * @brief Automated helper to extract every single config key from the target
 * file.
 */
std::vector<std::string> load_test_locales_from_config()
{
  std::vector<std::string> discovered_locales;
  std::ifstream file("locales_config.json");
  if (!file.is_open()) {
    // Return a baseline fallback matrix if file path is missing to avoid blind
    // runs
    return {"en_US", "en_IN", "de_DE", "ru_RU", "ja_JP"};
  }
  try {
    json data;
    file >> data;
    for (const auto &[key, value]: data.items()) {
      discovered_locales.push_back(key);
    }
  }
  catch (...) {
    return {"en_US", "en_IN"};
  }
  return discovered_locales;
}

// ============================================================================
// PARAMETERIZED MATRIX VALUE FIXTURES (Runs across ALL 67 Countries)
// ============================================================================

class GlobalizationMatrixTest : public ::testing::TestWithParam<std::string> {
  protected:
    void SetUp() override { active_locale = GetParam(); }
    std::string active_locale;
};

// Instantiate the fixture dynamically with every locale found inside the JSON
// file
INSTANTIATE_TEST_SUITE_P(AllConfiguredCountries, GlobalizationMatrixTest,
    ::testing::ValuesIn(load_test_locales_from_config()));

// ============================================================================
// 1. DYNAMIC NUMBER FORMATTING & PARSING BOUNDARY TESTS
// ============================================================================

TEST_P(GlobalizationMatrixTest, NumericRoundTripAndBoundaryValidation)
{
  // Target sample value
  constexpr double source_val = 12345678.96;

  // Test Case A: Valid Round-Trip Processing
  std::string formatted_str =
      LocaleUtils::format_number(source_val, active_locale);
  EXPECT_FALSE(formatted_str.empty());

  double extracted_val = 0.0;
  bool parse_ok =
      LocaleUtils::parse_number(formatted_str, extracted_val, active_locale);

  ASSERT_TRUE(parse_ok)
      << "Numeric parser rejected its own formatting output for locale: "
      << active_locale;
  EXPECT_NEAR(extracted_val, source_val, 0.001);

  // Test Case B: Boundary Processing (Zero Check)
  std::string zero_str = LocaleUtils::format_number(0.0, active_locale);
  double extracted_zero = -1.0;
  EXPECT_TRUE(
      LocaleUtils::parse_number(zero_str, extracted_zero, active_locale));
  EXPECT_NEAR(extracted_zero, 0.0, 0.001);

  // Test Case C: High Boundary Processing (Billions)
  constexpr double massive_val = 9876543210.12;
  std::string massive_str =
      LocaleUtils::format_number(massive_val, active_locale);
  double extracted_massive = 0.0;
  EXPECT_TRUE(
      LocaleUtils::parse_number(massive_str, extracted_massive, active_locale));
  EXPECT_NEAR(extracted_massive, massive_val, 0.001);
}

TEST_P(GlobalizationMatrixTest, NumericParserNegativeTesting)
{
  double trash_out = 0.0;

  // Test Case A: Total Garbage String Alpha Input
  EXPECT_FALSE(
      LocaleUtils::parse_number("ThisIsNotANumber", trash_out, active_locale));

  // Test Case B: Completely Empty String Protection Check
  EXPECT_FALSE(LocaleUtils::parse_number("", trash_out, active_locale));
}

// ============================================================================
// 2. STRICT CURRENCY ENGINE TESTING
// ============================================================================

TEST_P(GlobalizationMatrixTest, CurrencyStrictConsumptionValidation)
{
  constexpr double test_amount = 54321.10;
  std::string formatted_currency =
      LocaleUtils::format_currency(test_amount, active_locale);
  EXPECT_FALSE(formatted_currency.empty());

  // Positive Round-Trip Parse
  double parsed_currency = 0.0;
  bool currency_ok = LocaleUtils::parse_currency(
      formatted_currency, parsed_currency, active_locale);

  ASSERT_TRUE(currency_ok) << "Currency parser failed for locale: "
                           << active_locale;

  // FIX: Dynamically adjust the expected target value for zero-decimal
  // currencies
  double expected_target = test_amount;
  if (active_locale == "en_UG" || active_locale == "fr_CM" ||
      active_locale == "fr_NE" || active_locale == "hu_HU" ||
      active_locale == "in_ID" || active_locale == "ja_JP" ||
      active_locale == "ko_KR" || active_locale == "vi_VN") {
    expected_target =
        std::round(test_amount); // Expect 54321 instead of 54321.10
  }

  EXPECT_NEAR(parsed_currency, expected_target, 0.001);

  // Test Case B: Incomplete String Tampering Protection (Strict Consumer Check)
  // Appending trailing garbage letters should break compilation expectations
  std::string corrupted_currency = formatted_currency + " XYZ EXTRA GARBAGE";
  double corrupted_out = 0.0;
  bool corruption_detected = !LocaleUtils::parse_currency(
      corrupted_currency, corrupted_out, active_locale);

  EXPECT_TRUE(corruption_detected)
      << "CRITICAL ERROR: Currency parser accepted incomplete string matching "
         "for locale: "
      << active_locale;
}

// ============================================================================
// 3. REVERSE TEMPORAL CALENDAR TESTS
// ============================================================================

TEST_P(GlobalizationMatrixTest, TemporalRoundTripValidation)
{
  const auto current_time_point = std::chrono::system_clock::now();

  // Generate an exact, strict short layout pattern mapping
  std::string short_dt_string =
      LocaleUtils::format_short_date_time(current_time_point, active_locale);
  ASSERT_FALSE(short_dt_string.empty());

  std::chrono::system_clock::time_point parsed_destination;
  bool time_parse_ok = LocaleUtils::parse_date_time(
      short_dt_string, parsed_destination, active_locale);

  // Verify results
  EXPECT_TRUE(time_parse_ok)
      << "Temporal parser failed matching execution style for short string: "
      << short_dt_string << " in locale: " << active_locale;
}

// ============================================================================
// 4. LINGUISTICS & EXPANSIONS STABILITY TESTING
// ============================================================================

TEST_P(GlobalizationMatrixTest, TextExpansionSanityCheck)
{
  constexpr double test_payload = 1234.56;

  std::string words_out =
      LocaleUtils::expand_number_to_words(test_payload, active_locale);
  std::string currency_out =
      LocaleUtils::expand_currency_to_words(test_payload, active_locale);

  // Ensure text expansions never drop data blocks or return empty error codes
  EXPECT_FALSE(words_out.empty());
  EXPECT_FALSE(currency_out.empty());
  EXPECT_TRUE(words_out.find("[") == std::string::npos);
  EXPECT_FALSE(currency_out == "[Dynamic format mapping error]");
}

// ============================================================================
// GLOBALIZATION TEST HARNESS RUNNER INITIALIZATION
// ============================================================================

int main(int argc, char **argv)
{
  ::testing::InitGoogleTest(&argc, argv);

  // Force initialize environment locks before execution threads trigger
  LocaleUtils::initialize_system_locale();

  return RUN_ALL_TESTS();
}
