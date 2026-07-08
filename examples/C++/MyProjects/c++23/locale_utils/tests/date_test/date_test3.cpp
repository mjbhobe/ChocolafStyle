// tests/date_test/date_test3.cpp
#include <chrono>
#include <print>
#include "locale_utils.h"

int main()
{
  LocaleUtils::initialize_system_locale();

  // A fixed instant so every reader sees the same numbers.
  const auto tp = std::chrono::sys_days{
      std::chrono::year{2026} / std::chrono::July / 8} +
      std::chrono::hours{11} + std::chrono::minutes{25};

  std::println("--- Round-trip: format_short_date_time() -> parse_date_time() ---");
  int failures = 0;
  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN", "ja_JP"}) {
    std::println("--- {} ---", locale_id);
    std::println("Full   : {}",
        LocaleUtils::format_date_time(tp, false, locale_id));
    std::println("Date   : {}",
        LocaleUtils::format_date_time(tp, true, locale_id));

    std::string short_dt = LocaleUtils::format_short_date_time(tp, locale_id);
    std::println("Short  : {}", short_dt);

    std::chrono::system_clock::time_point parsed_tp;
    bool ok = LocaleUtils::parse_date_time(short_dt, parsed_tp, locale_id);
    std::println("Parsed : round-trip {}", ok ? "OK" : "FAILED");
    if (!ok) ++failures;
  }

  std::println("\n--- Rejecting an impossible calendar date (Feb 31) ---");
  std::chrono::system_clock::time_point bogus_tp;
  bool bogus_ok =
      LocaleUtils::parse_date("02/31/26", bogus_tp, "en_US");
  std::println("parse_date(\"02/31/26\") -> {} ({})", bogus_ok,
      bogus_ok ? "unexpectedly succeeded" : "correctly rejected");
  if (bogus_ok) ++failures;

  std::println("\n--- Rejecting a partially-matched string ---");
  std::chrono::system_clock::time_point trailing_tp;
  bool trailing_ok =
      LocaleUtils::parse_date_time("07/08/26, 11:25 AM extra garbage",
          trailing_tp, "en_US");
  std::println("parse_date_time(\"...extra garbage\") -> {} ({})", trailing_ok,
      trailing_ok ? "unexpectedly succeeded" : "correctly rejected");
  if (trailing_ok) ++failures;

  std::println("\n{} check(s) failed.", failures);
  return failures == 0 ? 0 : 1;
}
