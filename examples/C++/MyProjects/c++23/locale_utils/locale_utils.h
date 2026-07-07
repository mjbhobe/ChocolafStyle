// ============================================================================
// locale_utils.h - Universal multi-platform i18n utility interface
// Compatible with C++23 (GCC, Clang, MSVC) on Windows, Linux, and macOS.
// ============================================================================
#pragma once

#include <chrono>
#include <string>
#include <vector>

namespace LocaleUtils {

  // Automatically synchronizes standard runtime streams (std::cout/cin)
  // with the active Host Operating System language context.
  bool initialize_system_locale();

  // ------------------------------------------------------------------------
  // I/O Formatting & Parsing Engine
  // ------------------------------------------------------------------------
  std::string format_number(double value, const std::string &locale_name = "");
  bool parse_number(const std::string &input, double &out_value,
      const std::string &locale_name = "");

  std::string format_currency(
      double value, const std::string &locale_name = "");

  std::string format_date_time(const std::chrono::system_clock::time_point &tp,
      bool date_only = false, const std::string &locale_name = "");

  /**
   * @brief Formats a time point using strict short layout notations (e.g.,
   * MM/DD/YY).
   */
  std::string format_short_date_time(std::chrono::system_clock::time_point time,
      const std::string &locale_name);

  // ------------------------------------------------------------------------
  // Advanced Lingual Text Expansion (Powered by ICU)
  // ------------------------------------------------------------------------

  // Translates 123456 -> "one hundred twenty-three thousand four hundred
  // fifty-six"
  std::string expand_number_to_words(
      double value, const std::string &locale_name = "");

  // Translates 123456.78 -> "twelve thousand three hundred forty-five dollars
  // and seventy-eight cents" Handles Lakh/Crore systems natively when en_IN or
  // hi_IN is targeted.
  std::string expand_currency_to_words(
      double amount, const std::string &locale_name = "");

  /**
   * @brief Parses a localized currency string back into a raw double
   * floating-point value.
   * @param currency_str The source currency string (e.g., "$12,345.67" or "12
   * 345,67 €").
   * @param out_value Reference to store the extracted numeric value payload.
   * @param locale_name The targeted target identifier string profile.
   * @return true if string mapping was completely clean and valid, false
   * otherwise.
   */
  bool parse_currency(const std::string &currency_str, double &out_value,
      const std::string &locale_name);

  /**
   * @brief Parses a localized calendar date string into a standard chrono
   * system time point.
   * @param date_str The source date string structure (e.g., "06/07/2026",
   * "06.07.2026").
   * @param out_time Reference to store the calculated system clock point
   * destination.
   * @param locale_name The targeted target identifier string profile.
   * @return true if date composition properties completely validate, false
   * otherwise.
   */
  bool parse_date(const std::string &date_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name);

  /**
   * @brief Parses a localized date-time string containing time components into
   * a chrono point.
   * @param date_time_str The full source payload string (e.g., "Jul 6, 2026,
   * 11:25 AM").
   * @param out_time Reference to store the calculated system clock point
   * destination.
   * @param locale_name The targeted target identifier string profile.
   * @return true if complete pattern matching evaluates cleanly, false
   * otherwise.
   */
  bool parse_date_time(const std::string &date_time_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name);


} // namespace LocaleUtils
