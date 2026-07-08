// tests/date_test/date_test_calendar.cpp
#include <chrono>
#include <print>
#include "locale_utils.h"

int main() {
  LocaleUtils::initialize_system_locale();
  const auto tp =
      std::chrono::sys_days{std::chrono::year{2026} / std::chrono::July / 8};

  std::println("ja_JP (default)         : {}",
      LocaleUtils::format_date_time(tp, true, "ja_JP"));
  std::println("ja_JP@calendar=japanese : {}",
      LocaleUtils::format_date_time(tp, true, "ja_JP@calendar=japanese"));
  std::println("th_TH (default)         : {}",
      LocaleUtils::format_date_time(tp, true, "th_TH"));
}
