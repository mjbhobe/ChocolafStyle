// tests/date_test/date_test4.cpp
#include <chrono>
#include <print>
#include "locale_utils.h"

int main() {
  LocaleUtils::initialize_system_locale();

  // A fixed instant so every reader sees the same calendar date;
  // the clock reading itself renders in the host machine's local timezone.
  const auto tp = std::chrono::sys_days{
      std::chrono::year{2026} / std::chrono::July / 8} +
      std::chrono::hours{11} + std::chrono::minutes{25};

  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN"}) {
    std::println("--- {} ---", locale_id);
    std::println("Full   : {}",
        LocaleUtils::format_date_time(tp, false, locale_id));
    std::println("Date   : {}",
        LocaleUtils::format_date_time(tp, true, locale_id));

    std::string short_dt = LocaleUtils::format_short_date_time(tp, locale_id);
    std::println("Short  : {}", short_dt);

    std::chrono::system_clock::time_point parsed_tp;
    bool ok = LocaleUtils::parse_date_time(short_dt, parsed_tp, locale_id);
    std::println("Parsed : round-trip {}\n", ok ? "OK" : "FAILED");
  }
}
