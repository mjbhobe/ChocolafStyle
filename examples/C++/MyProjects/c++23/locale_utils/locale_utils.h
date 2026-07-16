// ============================================================================
// locale_utils.h - Universal multi-platform i18n utility interface
// Compatible with C++17 (GCC, Clang, MSVC) on Windows, Linux, and macOS.
//
// @author: Manish Bhobe
// My experiments with C/C++, STL, Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// ============================================================================
#pragma once

#include <chrono>
#include <string>
#include <vector>

namespace LocaleUtils {

  /**
   * @brief Automatically synchronizes standard runtime streams (std::cout/cin)
   * with the active Host Operating System language context.
   * @return true if the system locale was successfully applied, false
   * otherwise.
   */
  bool initialize_system_locale();

  // ------------------------------------------------------------------------
  // I/O Formatting & Parsing Engine
  // ------------------------------------------------------------------------

  /**
   * @brief Formats a numeric value using locale-aware grouping and decimal
   * separators.
   * @param value The numeric value to format.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return The formatted number as a string.
   */
  std::string format_number(double value, const std::string &locale_name = "");

  /**
   * @brief Parses a locale-formatted numeric string into a raw double value.
   * @param input The source numeric string (e.g., "12,345.67").
   * @param out_value Reference to store the extracted numeric value.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return true if the string was parsed successfully, false otherwise.
   */
  bool parse_number(const std::string &input, double &out_value,
      const std::string &locale_name = "");

  /**
   * @brief Formats a numeric value as a locale-aware currency string.
   * @param value The numeric amount to format.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return The formatted currency string.
   */
  std::string format_currency(
      double value, const std::string &locale_name = "");

  /**
   * @brief Formats a chrono time point using the locale's full date and time
   * layout.
   * @param tp The source time point to format.
   * @param date_only If true, only the date portion is formatted.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return The formatted date/time string.
   */
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

  /**
   * @brief Expands a numeric value into its full lingual word representation
   * (e.g., 123456 -> "one hundred twenty-three thousand four hundred
   * fifty-six").
   * @param value The numeric value to expand.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return The number spelled out in words.
   */
  std::string expand_number_to_words(
      double value, const std::string &locale_name = "");

  /**
   * @brief Expands a currency amount into its full lingual word
   * representation (e.g., 123456.78 -> "twelve thousand three hundred
   * forty-five dollars and seventy-eight cents"). Handles Lakh/Crore systems
   * natively when en_IN or hi_IN is targeted.
   * @param amount The currency amount to expand.
   * @param locale_name The targeted locale identifier string (empty for
   * system default).
   * @return The currency amount spelled out in words.
   */
  std::string expand_currency_to_words(
      double amount, const std::string &locale_name = "");

  /**
   * @brief Parses a localized currency string back into a raw double
   * floating-point value.
   * @param currency_str The source currency string (e.g., "$12,345.67" or "12
   * 345,67 €").
   * @param out_value Reference to store the extracted numeric value payload.
   * @param locale_name The targeted target identifier string profile  (empty for
   * system default).
   * @return true if string mapping was completely clean and valid, false
   * otherwise.
   */
  bool parse_currency(const std::string &currency_str, double &out_value,
      const std::string &locale_name = "");

  /**
   * @brief Parses a localized calendar date string into a standard chrono
   * system time point.
   * @param date_str The source date string structure (e.g., "06/07/2026",
   * "06.07.2026").
   * @param out_time Reference to store the calculated system clock point
   * destination.
   * @param locale_name The targeted target identifier string profile (empty for
   * system default).
   * @return true if date composition properties completely validate, false
   * otherwise.
   */
  bool parse_date(const std::string &date_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name = "");

  /**
   * @brief Parses a localized date-time string containing time components into
   * a chrono point.
   * @param date_time_str The full source payload string (e.g., "Jul 6, 2026,
   * 11:25 AM").
   * @param out_time Reference to store the calculated system clock point
   * destination.
   * @param locale_name The targeted target identifier string profile (empty for
   * system default).
   * @return true if complete pattern matching evaluates cleanly, false
   * otherwise.
   */
  bool parse_date_time(const std::string &date_time_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name = "");


} // namespace LocaleUtils
