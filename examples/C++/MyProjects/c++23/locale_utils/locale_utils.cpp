// ============================================================================
// locale_utils.cpp - Multi-platform i18n utility implementation
// ============================================================================
#include <cmath>
#include <fstream>
#include <iostream>
#include <locale>
#include <map>
#include <sstream>
#include "locale_utils.h"

// JSON parsing
#include <nlohmann/json.hpp>

// Primary ICU System Core Engine Headers
#include <unicode/locid.h>
#include <unicode/msgfmt.h>
#include <unicode/numfmt.h>
#include <unicode/rbnf.h>
#include <unicode/smpdtfmt.h>
#include <unicode/ucurr.h>

namespace LocaleUtils {

  bool initialize_system_locale()
  {
    try {
      std::locale user_loc("");
      std::locale::global(user_loc);
      std::cout.imbue(user_loc);
      std::cin.imbue(user_loc);
      std::cerr.imbue(user_loc);
      return true;
    }
    catch (...) {
      std::locale::global(std::locale::classic());
      return false;
    }
  }

  std::string format_number(double value, const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    std::unique_ptr<icu::NumberFormat> nf(
        icu::NumberFormat::createInstance(icu_loc, status));
    if (U_FAILURE(status))
      return std::to_string(value);

    icu::UnicodeString res;
    nf->format(value, res);
    std::string out;
    res.toUTF8String(out);
    return out;
  }

  bool parse_number(const std::string &input, double &out_value,
      const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    std::unique_ptr<icu::NumberFormat> nf(
        icu::NumberFormat::createInstance(icu_loc, status));
    if (U_FAILURE(status))
      return false;

    icu::Formattable result;
    icu::UnicodeString u_input = icu::UnicodeString::fromUTF8(input);
    nf->parse(u_input, result, status);

    if (U_FAILURE(status))
      return false;
    out_value = result.getDouble(status);
    return U_SUCCESS(status);
  }

  bool parse_currency(const std::string &currency_str, double &out_value,
      const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    std::unique_ptr<icu::NumberFormat> currency_parser(
        icu::NumberFormat::createCurrencyInstance(icu_loc, status));
    if (U_FAILURE(status))
      return false;

    icu::UnicodeString icu_input = icu::UnicodeString::fromUTF8(currency_str);
    icu::Formattable result_payload;
    icu::ParsePosition parse_pos(0);

    // Execute currency parsing
    currency_parser->parse(icu_input, result_payload, parse_pos);

    // CRITICAL FIX: Enforce absolute consumption.
    // If the parser stops before the end of the string, it is an incomplete
    // parsing failure.
    if (parse_pos.getIndex() != icu_input.length()) {
      return false;
    }

    out_value = result_payload.getDouble(status);
    return U_SUCCESS(status);
  }

  bool parse_date(const std::string &date_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    // Using kShort (e.g., MM/DD/YY or DD.MM.YY) to match generation patterns
    // perfectly
    std::unique_ptr<icu::DateFormat> date_parser(
        icu::DateFormat::createDateInstance(icu::DateFormat::kShort, icu_loc));
    if (date_parser == nullptr)
      return false;

    date_parser->setLenient(false); // Block invalid dates like Feb 31st

    icu::UnicodeString icu_input = icu::UnicodeString::fromUTF8(date_str);
    icu::ParsePosition parse_pos(0);

    UDate evaluated_epoch_ms = date_parser->parse(icu_input, parse_pos);

    // CRITICAL FIX: Enforce absolute consumption of the temporal layout string
    if (parse_pos.getIndex() != icu_input.length())
      return false;

    auto duration_since_epoch =
        std::chrono::milliseconds(static_cast<int64_t>(evaluated_epoch_ms));
    out_time = std::chrono::system_clock::time_point(duration_since_epoch);
    return true;
  }

  bool parse_date_time(const std::string &date_time_str,
      std::chrono::system_clock::time_point &out_time,
      const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    // Match the layout signature exactly with kShort, kShort configurations
    std::unique_ptr<icu::DateFormat> date_time_parser(
        icu::DateFormat::createDateTimeInstance(
            icu::DateFormat::kShort, icu::DateFormat::kShort, icu_loc));
    if (date_time_parser == nullptr)
      return false;

    date_time_parser->setLenient(false);

    icu::UnicodeString icu_input = icu::UnicodeString::fromUTF8(date_time_str);
    icu::ParsePosition parse_pos(0);

    UDate evaluated_epoch_ms = date_time_parser->parse(icu_input, parse_pos);

    // CRITICAL FIX: Enforce absolute consumption
    if (parse_pos.getIndex() != icu_input.length())
      return false;

    auto duration_since_epoch =
        std::chrono::milliseconds(static_cast<int64_t>(evaluated_epoch_ms));
    out_time = std::chrono::system_clock::time_point(duration_since_epoch);
    return true;
  }

  std::string format_currency(double value, const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    std::unique_ptr<icu::NumberFormat> nf(
        icu::NumberFormat::createCurrencyInstance(icu_loc, status));
    if (U_FAILURE(status))
      return std::to_string(value);

    icu::UnicodeString res;
    nf->format(value, res);
    std::string out;
    res.toUTF8String(out);
    return out;
  }

  std::string format_date_time(const std::chrono::system_clock::time_point &tp,
      bool date_only, const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    icu::DateFormat::EStyle style = icu::DateFormat::kMedium;
    std::unique_ptr<icu::DateFormat> df(date_only
            ? icu::DateFormat::createDateInstance(style, icu_loc)
            : icu::DateFormat::createDateTimeInstance(style, style, icu_loc));

    if (U_FAILURE(status))
      return "";

    UDate u_date = static_cast<UDate>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            tp.time_since_epoch())
            .count());
    icu::UnicodeString res;
    df->format(u_date, res);
    std::string out;
    res.toUTF8String(out);
    return out;
  }

  std::string format_short_date_time(std::chrono::system_clock::time_point time,
      const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    std::unique_ptr<icu::DateFormat> short_gen(
        icu::DateFormat::createDateTimeInstance(
            icu::DateFormat::kShort, icu::DateFormat::kShort, icu_loc));
    if (short_gen == nullptr)
      return "";

    UDate epoch_ms = static_cast<UDate>(
        std::chrono::duration_cast<std::chrono::milliseconds>(
            time.time_since_epoch())
            .count());

    icu::UnicodeString icu_result;
    short_gen->format(epoch_ms, icu_result);

    std::string printable_output;
    icu_result.toUTF8String(printable_output);
    return printable_output;
  }

  /*
    std::string expand_number_to_words(
        double value, const std::string &locale_name)
    {
      UErrorCode status = U_ZERO_ERROR;
      icu::Locale icu_loc = locale_name.empty()
          ? icu::Locale::getDefault()
          : icu::Locale(locale_name.c_str());

      icu::RuleBasedNumberFormat formatter(icu::URBNF_SPELLOUT, icu_loc,
    status); if (U_FAILURE(status)) return "[Spellout conversion failed]";

      icu::UnicodeString res;
      formatter.format(value, res);
      std::string out;
      res.toUTF8String(out);
      return out;
    }
  */

  bool load_external_json_profile(const std::string &locale_id,
      std::string &major_s, std::string &major_p, std::string &minor_s,
      std::string &minor_p, std::string &conjunction)
  {
    std::ifstream file("locales_config.json");
    if (!file.is_open())
      return false;

    try {
      nlohmann::json config_data;
      file >> config_data;

      if (!config_data.contains(locale_id))
        return false;

      auto profile = config_data[locale_id];
      major_s = profile.value("major_s", "unit");
      major_p = profile.value("major_p", "units");
      minor_s = profile.value("minor_s", "");
      minor_p = profile.value("minor_p", "");
      conjunction = profile.value("conj", "and");
      return true;
    }
    catch (...) {
      return false;
    }
  }

  // ... format_number, parse_number, format_currency, format_date_time
  // implementations remain as previously provided ...

  std::string expand_number_to_words(
      double value, const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());

    icu::RuleBasedNumberFormat formatter(icu::URBNF_SPELLOUT, icu_loc, status);
    if (U_FAILURE(status))
      return "[Spellout conversion failed]";

    icu::UnicodeString res;
    formatter.format(value, res);
    std::string out;
    res.toUTF8String(out);
    return out;
  }

  std::string expand_currency_to_words(
      double amount, const std::string &locale_name)
  {
    UErrorCode status = U_ZERO_ERROR;
    icu::Locale icu_loc = locale_name.empty()
        ? icu::Locale::getDefault()
        : icu::Locale(locale_name.c_str());
    std::string active_locale_str = icu_loc.getName();

    std::string major_s, major_p, minor_s, minor_p, conjunction;
    if (!load_external_json_profile(active_locale_str, major_s, major_p,
            minor_s, minor_p, conjunction)) {
      major_s = "unit";
      major_p = "units";
      minor_s = "sub-unit";
      minor_p = "sub-units";
      conjunction = "and";
    }

    double int_part_raw;
    double frac_part_raw = std::round(std::modf(amount, &int_part_raw) * 100.0);
    int64_t major_units = static_cast<int64_t>(int_part_raw);
    int64_t minor_units = static_cast<int64_t>(std::abs(frac_part_raw));

    std::string major_words = expand_number_to_words(
        static_cast<double>(major_units), active_locale_str);
    std::string minor_words = expand_number_to_words(
        static_cast<double>(minor_units), active_locale_str);

    std::string pattern_str =
        "{0} {1, plural, one{" + major_s + "} other{" + major_p + "}}";

    if (!minor_s.empty() && minor_units > 0) {
      pattern_str += " " + conjunction + " {2} {3, plural, one{" + minor_s +
          "} other{" + minor_p + "}}";
    }

    icu::UnicodeString icu_pattern(pattern_str.c_str());
    icu::MessageFormat msg_formatter(icu_pattern, icu_loc, status);
    if (U_FAILURE(status))
      return "[Dynamic format mapping error]";

    icu::Formattable arguments[] = {icu::UnicodeString::fromUTF8(major_words),
        (int64_t) major_units, icu::UnicodeString::fromUTF8(minor_words),
        (int64_t) minor_units};

    icu::UnicodeString final_icu_result;
    icu::FieldPosition fp(icu::FieldPosition::DONT_CARE);
    msg_formatter.format(arguments, 4, final_icu_result, fp, status);

    std::string result_text;
    final_icu_result.toUTF8String(result_text);
    return result_text;
  }
} // namespace LocaleUtils
