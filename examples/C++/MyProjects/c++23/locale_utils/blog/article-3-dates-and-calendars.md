## Locale-Aware C++: Building Globally-Correct Console Applications — Part 3: Dates & Calendars

### Why `2026-07-08` is not a date anyone actually writes

Parts 1 and 2 fixed numbers and currency. Dates look like they should be the easy one — until you print one:

```cpp
// tests/date_test/date_test1.cpp
#include <chrono>
#include <iostream>

int main() {
    using namespace std::chrono;
    auto tp = sys_days{2026y / July / 8};

    std::cout << "Date: " << tp << '\n';
    return 0;
}
```

```
Date: 2026-07-08
```

That's C++20/23's `std::chrono` calendar support working exactly as documented — `operator<<` on a `sys_days` always emits ISO 8601, full stop. There's no ambiguity to argue about here, because there's no attempt at localization at all: an American reader, a French reader, and a Russian reader all see the identical string, and *none* of them would write the date that way on a form, an invoice, or an email.

Here's what each of them actually expects, for the same instant our series has used throughout — this time as a calendar date instead of a plain number:

| Locale | Expected short date | Expected full date |
|---|---|---|
| USA (`en_US`) | `7/8/26` | `Jul 8, 2026` |
| France (`fr_FR`) | `08/07/2026` | `8 juil. 2026` |
| Russia (`ru_RU`) | `08.07.2026` | `8 июл. 2026 г.` |
| India (`en_IN`) | `08/07/26` | `8 Jul 2026` |

Notice the day/month order flips between the US and everyone else, the separator changes (`/` vs `.`), Russia appends a trailing `г.` ("goda" — "of the year"), and the month name itself is a different alphabet entirely for Russian. None of that is guessable from a `year_month_day` alone; it has to come from real locale data, same as Parts 1 and 2.

---

### Why `std::chrono`'s own locale-aware formatting doesn't get you there

C++20 gave `std::chrono` formatter specs that are supposed to be locale-sensitive — `%x` for the locale's date representation, `%A`/`%B` for localized weekday and month names — driven by an explicit `std::locale` you pass to `std::format`:

```cpp
// tests/date_test/date_test2.cpp
#include <chrono>
#include <iostream>
#include <locale>

int main() {
    using namespace std::chrono;
    auto tp = sys_days{2026y / July / 8};

    for (const auto &locale_name : {"en_US.utf8", "fr_FR.utf8", "ru_RU.utf8", "de_DE.utf8"}) {
        std::locale loc(locale_name);
        std::cout << locale_name
                   << " -> %x=" << std::format(loc, "{:%x}", tp)
                   << " %A=" << std::format(loc, "{:%A}", tp)
                   << " %B=" << std::format(loc, "{:%B}", tp) << '\n';
    }
    return 0;
}
```

Every one of `en_US.utf8`, `fr_FR.utf8`, `ru_RU.utf8`, and `de_DE.utf8` is genuinely installed on this machine (`locale -a` confirms it), and none of the four calls throw. Yet here's what it actually prints, verified on both GCC 16 and Clang 22 with libstdc++'s `<chrono>`:

```
en_US.utf8 -> %x=07/08/26 %A=Wednesday %B=July
fr_FR.utf8 -> %x=07/08/26 %A=Wednesday %B=July
ru_RU.utf8 -> %x=07/08/26 %A=Wednesday %B=July
de_DE.utf8 -> %x=07/08/26 %A=Wednesday %B=July
```

Identical output for all four locales. This isn't a typo in the demo or a misunderstanding of `%x` — the locale-aware chrono conversion specifiers silently no-op back to the `"C"` locale's English/US formatting in the widely-used libstdc++ implementation, instead of erroring or falling back loudly. Part 1 and Part 2's number and currency facets (`std::numpunct`, `std::moneypunct`, `{:L}`) at least *worked* once a matching locale was installed; `<chrono>`'s locale-aware date formatting, at least on this toolchain, currently doesn't work even then.

And even where it does work on some platform, `<chrono>`'s calendar types (`year_month_day` and friends) are pure proleptic-Gregorian. There is no standard-library concept of:

- **Non-Gregorian calendars** — Japan's imperial era (令和/Reiwa), Thailand's Buddhist calendar, the Hijri calendar used across much of the Middle East.
- **Grammatically-inflected month/weekday names** — some languages change the *form* of a month name depending on whether it stands alone or is followed by a day number (more on this below).

Same conclusion as Parts 1 and 2: for identical behavior across Manjaro, Ubuntu, Fedora, macOS, and Windows, we route dates through ICU too.

---

### `format_date_time`, `format_short_date_time`, and their parsers

`format_date_time` asks ICU for a date or date-time instance at `kMedium` style and lets CLDR's locale data pick the order, separators, and month/weekday names:

```cpp
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
```

`format_short_date_time` is the same idea pinned to `kShort` style, because a short, unambiguous layout is what we need to feed back into a parser:

```cpp
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
```

`parse_date` and `parse_date_time` mirror the strict-consumption discipline Parts 1 and 2 established for numbers and currency — and add one more guard specific to calendars, `setLenient(false)`:

```cpp
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
```

Without `setLenient(false)`, ICU's default behavior is to *roll over* an invalid date instead of rejecting it — `"02/31/26"` would silently become March 3rd rather than failing. That's exactly the kind of quietly-wrong behavior this series keeps calling out: a calendar library should refuse a date that never existed, not guess what the caller "probably meant." `parse_date_time` (used for full date-time strings like `"7/8/26, 4:55 PM"`) applies the identical two guards against its own `kShort`/`kShort` date-time instance.

---

### Proving it works: a round-trip test

`tests/date_test/date_test3.cpp` formats our recurring instant across four locales, round-trips each short string back through `parse_date_time`, then throws two failure cases at the parsers: an impossible calendar date and a string with trailing garbage.

```cpp
// tests/date_test/date_test3.cpp
#include <chrono>
#include <print>
#include "locale_utils.h"

int main()
{
  LocaleUtils::initialize_system_locale();

  const auto tp = std::chrono::sys_days{
      std::chrono::year{2026} / std::chrono::July / 8} +
      std::chrono::hours{11} + std::chrono::minutes{25};

  int failures = 0;
  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN", "ja_JP"}) {
    std::println("--- {} ---", locale_id);
    std::println("Full   : {}",
        LocaleUtils::format_date_time(tp, false, locale_id));

    std::string short_dt = LocaleUtils::format_short_date_time(tp, locale_id);
    std::println("Short  : {}", short_dt);

    std::chrono::system_clock::time_point parsed_tp;
    bool ok = LocaleUtils::parse_date_time(short_dt, parsed_tp, locale_id);
    std::println("Parsed : round-trip {}", ok ? "OK" : "FAILED");
    if (!ok) ++failures;
  }

  std::chrono::system_clock::time_point bogus_tp;
  bool bogus_ok = LocaleUtils::parse_date("02/31/26", bogus_tp, "en_US");
  std::println("\nparse_date(\"02/31/26\") -> {} ({})", bogus_ok,
      bogus_ok ? "unexpectedly succeeded" : "correctly rejected");
  if (bogus_ok) ++failures;

  std::chrono::system_clock::time_point trailing_tp;
  bool trailing_ok = LocaleUtils::parse_date_time(
      "07/08/26, 11:25 AM extra garbage", trailing_tp, "en_US");
  std::println("parse_date_time(\"...extra garbage\") -> {} ({})", trailing_ok,
      trailing_ok ? "unexpectedly succeeded" : "correctly rejected");
  if (trailing_ok) ++failures;

  std::println("\n{} check(s) failed.", failures);
  return failures == 0 ? 0 : 1;
}
```

Build and run it from `tests/date_test/` the same way the earlier articles' tests were built:

```bash
cmake -S . -B build -DCMAKE_CXX_COMPILER=clang++
cmake --build build --target date_test3
./build/date_test3
```

Which produces:

```
--- en_US ---
Full   : Jul 8, 2026, 4:55:00 PM
Short  : 7/8/26, 4:55 PM
Parsed : round-trip OK
--- fr_FR ---
Full   : 8 juil. 2026, 16:55:00
Short  : 08/07/2026 16:55
Parsed : round-trip OK
--- ru_RU ---
Full   : 8 июл. 2026 г., 16:55:00
Short  : 08.07.2026, 16:55
Parsed : round-trip OK
--- en_IN ---
Full   : 8 Jul 2026, 4:55:00 pm
Short  : 08/07/26, 4:55 pm
Parsed : round-trip OK
--- ja_JP ---
Full   : 2026/07/08 16:55:00
Short  : 2026/07/08 16:55
Parsed : round-trip OK

parse_date("02/31/26") -> false (correctly rejected)
parse_date_time("...extra garbage") -> false (correctly rejected)

0 check(s) failed.
```

(The clock reading — `4:55 PM` / `16:55` — renders in whatever timezone the host machine is set to; this run was on an IST machine, five and a half hours ahead of the `11:25` UTC instant baked into the source. The calendar date and the locale-correct ordering, separators, and month names are the part that matters, and they're identical regardless of timezone.)

Five locales, one code path, and both failure cases rejected instead of silently coerced — same discipline Parts 1 and 2 established for numbers and currency.

---

### A real-world gotcha: calendars and grammar don't always follow the locale you'd guess

**First, calendars and eras.** Japan and Thailand both have their own traditional calendars, but CLDR doesn't opt every locale into its "home" calendar by default — and it doesn't do it consistently:

```cpp
// tests/date_test/date_test_calendar.cpp
LocaleUtils::format_date_time(tp, true, "ja_JP");                      // Gregorian
LocaleUtils::format_date_time(tp, true, "ja_JP@calendar=japanese");    // Imperial era
LocaleUtils::format_date_time(tp, true, "th_TH");                      // Buddhist (default!)
```

```
ja_JP (default)         : 2026/07/08
ja_JP@calendar=japanese : 令和8年7月8日
th_TH (default)         : 8 ก.ค. 2569
```

`th_TH`'s default *is* the Buddhist calendar — `2569` (2026 + 543 years), no extension needed. `ja_JP`'s default is plain Gregorian; the imperial era (令和8年 — "Reiwa year 8") only appears if the caller explicitly appends `@calendar=japanese` to the locale name. There's no way to guess this asymmetry from either locale's name — one locale defaults to its traditional calendar, the other doesn't, and both are "correct" per CLDR. **A known limitation worth stating plainly:** `LocaleUtils`'s current interface takes a bare `locale_name` string and passes it straight through to `icu::Locale`, so a caller who needs imperial-era Japanese dates *can* get them — but only by knowing to append the ICU locale extension themselves. A more complete API would expose a `calendar` parameter with sane per-country defaults, rather than requiring callers to already know ICU's extension syntax.

**Second, month names change form depending on grammatical context.** Ask ICU for a Russian month name two different ways:

```cpp
icu::SimpleDateFormat format_pattern(icu::UnicodeString("d MMMM y"), ru_locale, status);   // "format" context
icu::SimpleDateFormat standalone_pattern(icu::UnicodeString("LLLL"), ru_locale, status);   // "stand-alone" context
```

```
explicit 'd MMMM y': 8 июля 2026     (genitive — "of July")
explicit 'LLLL'    : июль             (nominative — "July")
```

`MMMM` and `LLLL` both mean "full month name" — but `MMMM` is the *format* context (the month name as it appears attached to a day number, grammatically inflected) while `LLLL` is the *stand-alone* context (the month name as you'd see it as a dictionary entry or a calendar-grid header). Russian, like many Slavic languages, genuinely uses different words for these two cases: `июля` ("of July," genitive) versus `июль` ("July," nominative). `format_date_time` and `format_short_date_time` use ICU's `createDateInstance`/`createDateTimeInstance` factories, which correctly select the format (genitive) context for us — so the round-trip demo above already gets this right. The trap is for code that *doesn't* go through those factories: a naive calendar-header widget built by reusing the same `"MMMM"` pattern to print a lone month label would silently emit grammatically wrong text, the same quiet-but-fluent failure mode Part 2 found in Russian plural categories.

---

### Putting it together: four locales, one code path

```cpp
// tests/date_test/date_test4.cpp
#include <chrono>
#include <print>
#include "locale_utils.h"

int main() {
  LocaleUtils::initialize_system_locale();

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
```

Running it produces:

```
--- en_US ---
Full   : Jul 8, 2026, 4:55:00 PM
Date   : Jul 8, 2026
Short  : 7/8/26, 4:55 PM
Parsed : round-trip OK

--- fr_FR ---
Full   : 8 juil. 2026, 16:55:00
Date   : 8 juil. 2026
Short  : 08/07/2026 16:55
Parsed : round-trip OK

--- ru_RU ---
Full   : 8 июл. 2026 г., 16:55:00
Date   : 8 июл. 2026 г.
Short  : 08.07.2026, 16:55
Parsed : round-trip OK

--- en_IN ---
Full   : 8 Jul 2026, 4:55:00 pm
Date   : 8 Jul 2026
Short  : 08/07/26, 4:55 pm
Parsed : round-trip OK
```

Day/month order, separators, the trailing `г.`, AM/PM case — all four locales fall out of the same four `LocaleUtils` calls, with no `if (locale == "ru_RU")` in application code.

---

### Summary

- `std::chrono`'s default stream output for calendar types is always ISO 8601 — no localization is attempted at all.
- `std::chrono`'s locale-aware format specifiers (`%x`, `%A`, `%B`) accept an explicit `std::locale`, but on the widely-used libstdc++ implementation (verified here on both GCC 16 and Clang 22), they silently ignore it and fall back to English/US output — a real, reproducible gap, not a hypothetical one.
- `std::chrono`'s calendar types are pure proleptic-Gregorian; there's no standard-library concept of Japan's imperial era, Thailand's Buddhist calendar, or any other calendar system.
- `format_date_time` / `format_short_date_time` and `parse_date` / `parse_date_time` route everything through ICU's `DateFormat`, giving locale-correct order, separators, and month/weekday names, plus strict rejection of both impossible calendar dates (`setLenient(false)`) and partially-matched input strings — the same discipline as Parts 1 and 2's parsers.
- A genuine, verified gotcha surfaced on both fronts the teaser promised: CLDR doesn't consistently opt locales into their "home" calendar (Thai defaults to Buddhist, Japanese doesn't default to imperial), and ICU's month-name patterns distinguish a grammatically-inflected "format" context (`MMMM`) from a dictionary "stand-alone" context (`LLLL`) — a distinction our factory-based functions get right automatically, but that a naive direct-pattern implementation could easily get wrong.

**Next up — Part 4:** we step back from adding features and ask how you'd actually trust this library — a GoogleTest matrix that runs every check across all 68 configured locales at once, and what it takes to keep that matrix honest as the locale list grows.
