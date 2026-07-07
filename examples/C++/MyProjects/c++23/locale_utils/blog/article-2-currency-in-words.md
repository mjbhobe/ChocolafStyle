## Locale-Aware C++: Building Globally-Correct Console Applications — Part 2: Currency

### Why `$34,573,892,785.34` is three bugs waiting to happen

Part 1 fixed how we display and parse plain numbers. Currency looks like the same problem wearing a different hat — until you try it:

```cpp
#include <iostream>

int main() {
    constexpr double amount = 34573892785.34;
    std::cout << "$" << amount << '\n';
    return 0;
}
```

Three things are wrong before we've even left `main()`. First, the `$` is hardcoded — this program can never show a Euro, a Ruble, or a Rupee without a rewrite. Second, `std::cout`'s default float formatting still applies, so large amounts collapse into `3.45739e+10` exactly as in Part 1. Third — and this is the one that's easy to miss — even a "fixed" version with the right symbol and grouping is still wrong for large parts of the world, because **currency isn't just a number with a symbol glued on**:

| Locale | Correct display | Notes |
|---|---|---|
| USA (`en_US`) | `$34,573,892,785.34` | 2 decimal digits (cents) |
| France (`fr_FR`) | `34 573 892 785,34 €` | symbol *follows* the amount, space-separated |
| Russia (`ru_RU`) | `34 573 892 785,34 ₽` | symbol follows, space-grouped like French |
| India (`en_IN`) | `₹34,57,38,92,785.34` | lakh/crore grouping, symbol leads |

Symbol position, spacing, and grouping all vary independently per locale — and that's before we even get to currencies like the Japanese yen or Korean won, which have **zero** minor-unit digits, or the Kuwaiti dinar, which has **three**. None of this is guessable from the amount alone; it has to come from real locale and currency data.

---

### Why `moneypunct` doesn't close the gap

C++'s `<locale>` has a currency-formatting facet, `std::moneypunct`, and it does pick up the OS's grouping and symbol conventions once a matching locale is installed:

```cpp
std::locale loc("en_IN.utf8");
std::cout.imbue(loc);
std::cout << std::showbase << std::put_money(3457389278534L) << '\n';
// -> ₹34,57,38,92,785.34
```

That much actually works on this machine — so, to be precise about the critique (Part 1 argued `std::numpunct` can't express irregular grouping at all; for lakh/crore specifically, glibc's repeat-last-group encoding happens to cover it). What `moneypunct` — and the rest of `<locale>` — genuinely cannot do, in any locale, on any platform, is this:

- **It has no spellout facility.** Just like Part 1's `std::numpunct`, there is no standard-library path from `34573892785.34` to *"thirty-four billion ... dollars and thirty-four cents"* — not in English, not in any language.
- **It has no notion of grammatical number.** "1 dollar" vs. "2 dollars" is a plural-agreement problem, not a formatting-punctuation problem, and `<locale>` was never designed to answer "what's the correct word for the unit name at this quantity, in this language."

Formatting the digits correctly (`format_currency`) and getting a locale-correct sentence out of an amount (`expand_currency_to_words`) are genuinely different problems. ICU gives us a clean path to both; the rest of this article builds them into `LocaleUtils`.

---

### `format_currency` and `parse_currency`

`format_currency` is one line different from Part 1's `format_number` — it asks ICU for a *currency* instance instead of a plain one, and ICU pulls the correct symbol, decimal-digit count, and grouping straight from CLDR:

```cpp
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
```

`parse_currency` mirrors it, and keeps the same discipline Part 1 established for `parse_number`: a partial match is a failure, not a best-effort guess.

```cpp
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
  currency_parser->parse(icu_input, result_payload, parse_pos);

  // CRITICAL FIX: Enforce absolute consumption. If the parser stops before
  // the end of the string, it is an incomplete parsing failure.
  if (parse_pos.getIndex() != icu_input.length())
    return false;

  out_value = result_payload.getDouble(status);
  return U_SUCCESS(status);
}
```

That's the entire display/round-trip story, and it's genuinely this short. The interesting engineering is in the next function.

---

### `expand_currency_to_words`: ICU spells the number, we supply the grammar

ICU's `RuleBasedNumberFormat` (the same spellout engine from Part 1) knows how to turn `34573892785` into words in dozens of languages. What it does **not** know is what to call the currency unit — "US Dollar" vs. "euro" vs. "российский рубль" vs. "Indian Rupee" isn't a property of the *locale*, it's a property of *which currency that locale's economy uses*, and it needs both a singular and a plural form.

So `LocaleUtils` externalizes that vocabulary into a JSON file, `locales_config.json`, one entry per locale, covering 69 locales across every populated continent and half a dozen scripts:

```json
{
  "en_US": { "major_s": "US Dollar", "major_p": "US Dollars", "minor_s": "cent", "minor_p": "cents", "conj": "and" },
  "fr_FR": { "major_s": "euro", "major_p": "euros", "minor_s": "centime", "minor_p": "centimes", "conj": "et" },
  "ru_RU": { "major_s": "российский рубль", "major_p": "российских рублей", "minor_s": "копейка", "minor_p": "копеек", "conj": "и" },
  "en_IN": { "major_s": "Indian Rupee", "major_p": "Indian Rupees", "minor_s": "paisa", "minor_p": "paise", "conj": "and" },
  "ja_JP": { "major_s": "日本円", "major_p": "日本円", "minor_s": "", "minor_p": "", "conj": "" }
}
```

Note `ja_JP`'s empty `minor_s`/`minor_p` — the yen has no subunit in ordinary use, so the code below simply omits the minor-unit clause whenever `minor_s` is empty, rather than printing "0 sen" nobody asked for. A small loader keeps the parsing (and its failure mode) contained to one function:

```cpp
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
```

With the vocabulary in hand, `expand_currency_to_words` splits the amount into major and minor **integer units first**, spells each with `expand_number_to_words`, and lets ICU's `MessageFormat` glue the sentence together with the correct plural form:

```cpp
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
    major_s = "unit"; major_p = "units";
    minor_s = "sub-unit"; minor_p = "sub-units";
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
```

Two design points worth calling out. First, `{1, plural, one{...} other{...}}` is ICU's plural-selection syntax: `MessageFormat` looks at the *number* argument (`major_units`), asks the locale's CLDR plural rules which grammatical category it falls into, and substitutes the matching branch — so `major_units == 1` correctly says "dollar" while everything else says "dollars," without an `if` anywhere in application code.

Second — and this is a quiet payoff from Part 1 — `major_units` and `minor_units` are always plain integers by the time they reach `expand_number_to_words`. That function's fractional part (`std::modf`) is therefore always exactly `0.0`, so it takes the early-return path and the IEEE-754-leaking stand-in logic from Part 1 never runs at all. Splitting currency into major/minor units wasn't just done for the "and NN cents" phrasing — it happens to make this function immune, by construction, to the exact floating-point/spellout bug Part 1 spent so much effort fixing.

---

### A real-world gotcha: two plural categories aren't always enough

English has two grammatical-number categories: singular and plural. ICU's `{plural, one{...} other{...}}` syntax, as used above, mirrors that. But most of the world's languages don't stop at two. Query ICU's actual plural rules for Russian:

```cpp
icu::PluralRules::forLocale(icu::Locale("ru_RU"), status)->select(value);
```

```
1  -> one
2  -> few
3  -> few
4  -> few
5  -> many
11 -> many
21 -> one
22 -> few
25 -> many
96 -> many
```

Russian (like Polish, Ukrainian, and most other Slavic and Baltic languages) has **four** categories — `one`, `few`, `many`, `other` — selected by a rule far more intricate than "is it 1?". Our `MessageFormat` pattern only ever defines `one` and `other`. ICU still correctly determines that `2` belongs to category `few` — but since `few` isn't a branch in our pattern, `MessageFormat` falls back to `other`, and the sentence comes out grammatically wrong without raising any error at all:

```cpp
LocaleUtils::expand_currency_to_words(2.0, "ru_RU");
// -> "два российских рублей"   (WRONG — should be "два российских рубля")
LocaleUtils::expand_currency_to_words(1.0, "ru_RU");
// -> "один российский рубль"   (correct — "one" category exists)
LocaleUtils::expand_currency_to_words(22.0, "ru_RU");
// -> "двадцать два российских рублей"   (WRONG — should be "...рубля")
```

This isn't a contrived edge case, either — it's already hiding inside this article's own headline example. `34573892785.34` has 34 kopecks, and 34 falls in the `few` category (it ends in 4, and Russian's rule excludes the 11–14 range from `few`):

```
Currency to Text : ... тридцать четыре копеек
```

`копеек` is the `many`/`other` form; the grammatically correct word for 34 kopecks is `копейки`. The output reads fluently enough that nothing about it looks broken — which is precisely what makes this class of bug more dangerous than a crash: a crash gets noticed and filed, wrong-but-fluent grammar ships quietly.

**A known limitation worth stating plainly**, in the same spirit as Part 1's Russian gender note: fixing this fully means extending `locales_config.json` with optional `few`/`many`/`zero` vocabulary slots for the dozen-or-so locales whose grammar needs them (Slavic and Baltic languages, Arabic, and others), and building the `MessageFormat` pattern's branch list conditionally per locale instead of hardcoding `one`/`other`. That's a real, scoped follow-up, not a fundamental limitation of the ICU/`MessageFormat` approach — the plural-category data ICU needs is already being computed correctly under the hood, as the `PluralRules` table above shows. We're just not yet asking our own pattern to use all of it.

---

### Putting it together: four locales, one code path

```cpp
#include <print>
#include "locale_utils.h"

int main() {
  LocaleUtils::initialize_system_locale();
  constexpr double amount = 34573892785.34;

  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN"}) {
    std::println("--- {} ---", locale_id);
    std::string displayed = LocaleUtils::format_currency(amount, locale_id);
    std::println("Display : {}", displayed);
    std::println("Spelled : {}",
        LocaleUtils::expand_currency_to_words(amount, locale_id));

    double parsed_value{};
    bool ok = LocaleUtils::parse_currency(displayed, parsed_value, locale_id);
    std::println("Parsed  : {} (round-trip {})",
        parsed_value, ok ? "OK" : "FAILED");
  }
}
```

Running it produces:

```
--- en_US ---
Display : $34,573,892,785.34
Spelled : thirty-four billion five hundred seventy-three million eight hundred
          ninety-two thousand seven hundred eighty-five US Dollars and thirty-four cents
Parsed  : 34573892785.34 (round-trip OK)

--- fr_FR ---
Display : 34 573 892 785,34 €
Spelled : trente-quatre milliards cinq cent soixante-treize millions huit cent
          quatre-vingt-douze mille sept cent quatre-vingt-cinq euros et trente-quatre centimes
Parsed  : 34573892785.34 (round-trip OK)

--- ru_RU ---
Display : 34 573 892 785,34 ₽
Spelled : тридцать четыре миллиарда пятьсот семьдесят три миллиона восемьсот
          девяносто две тысячи семьсот восемьдесят пять российских рублей и тридцать четыре копеек
Parsed  : 34573892785.34 (round-trip OK)

--- en_IN ---
Display : ₹34,57,38,92,785.34
Spelled : three thousand four hundred fifty-seven crore thirty-eight lakh
          ninety-two thousand seven hundred eighty-five Indian Rupees and thirty-four paise
Parsed  : 34573892785.34 (round-trip OK)
```

Display formatting, round-trip parsing, and spellout all go through the same four functions regardless of script, symbol position, or grouping rule — India's lakh/crore currency phrasing falls out of the same `expand_currency_to_words` call as everyone else's, with no `if (locale == "en_IN")` in sight.

---

### Summary

- Currency formatting is not "a number plus a symbol": symbol position, spacing, grouping, and decimal-digit count (0 for yen, 2 for dollars, 3 for Kuwaiti dinars) all vary independently per locale, and none of it is guessable from the amount.
- `std::moneypunct` can pick up some of this from the OS locale, but — like `std::numpunct` in Part 1 — it has no spellout facility at all, and no concept of grammatical plural agreement for the unit name.
- `format_currency` and `parse_currency` are thin, one-line-different siblings of Part 1's number functions, backed by ICU's currency-aware `NumberFormat`.
- `expand_currency_to_words` layers a small, externalized JSON vocabulary (`locales_config.json`, 69 locales) on top of ICU's spellout and `MessageFormat` plural selection, so the unit name and its singular/plural form come from data, not code.
- Splitting the amount into major/minor integer units — done here for the "N dollars and M cents" phrasing — has a welcome side effect: it keeps every call into `expand_number_to_words` free of a fractional part, sidestepping Part 1's floating-point/spellout bug entirely.
- A genuine, currently-shipping bug surfaced along the way: our `MessageFormat` pattern only defines the `one`/`other` plural categories, so locales needing `few`/`many` (Russian, Polish, Ukrainian, and others) silently fall back to the wrong grammatical form — visible in this very article's own worked example ("копеек" instead of "копейки" for 34 kopecks). It's flagged here, not fixed, in the same spirit as Part 1's Russian gender limitation: professional software says what it doesn't yet handle.

**Next up — Part 3:** dates. We'll extend `LocaleUtils` to format and parse calendar dates correctly across locales — where the hard part isn't just `DD/MM` vs. `MM/DD`, but calendars, era names, and weekday-name grammar that vary as much as currency vocabulary does.
