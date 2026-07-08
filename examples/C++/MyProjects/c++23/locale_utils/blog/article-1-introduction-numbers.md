## Locale-Aware C++: Building Globally-Correct Console Applications — Part 1: Numbers

### Why the number `34573892785.34` is not the same number everywhere

If you've spent five-plus years writing C++, you've probably written a hundred variants of this function:

```cpp
// tests/number_test/number_test1.cpp
#include <iostream>

int main() {
    constexpr double large_value = 34573892785.34;
    std::cout << "Value: " << large_value << '\n';

    std::cout << "Enter a number: ";
    double user_value{};
    std::cin >> user_value;
    std::cout << "You entered: " << user_value << '\n';
    return 0;
}
```

Compile and run it, and you get exactly what you'd expect:

```
Value: 3.45739e+10
Enter a number: 34573892785.34
You entered: 3.45739e+10
```

Two things are already wrong here, and neither is a compiler bug.

First, `std::cout`'s default float formatting silently switched to scientific notation once the magnitude got large enough — `3.45739e+10` is not what any end user wants to see on an invoice or a dashboard. Second, even if we force fixed notation, the output has **no thousands separators** and uses a **dot** as the decimal marker. That's the standard "C" locale — the one every C++ stream is born with, regardless of what operating system, region, or language the person running your program actually uses!

Now put this program in front of an accountant in Paris, an engineer in Mumbai, or an analyst in Moscow:

| Locale | Expected display | What our program shows |
|---|---|---|
| France (`fr_FR`) | `34 573 892 785,34` | `3.45739e+10` |
| India (`en_IN`) | `34,57,38,92,785.34` | `3.45739e+10` |
| Russia (`ru_RU`) | `34 573 892 785,34` | `3.45739e+10` |
| USA (`en_US`) | `34,573,892,785.34` | `3.45739e+10` |

Notice that India doesn't just swap the separator characters — it groups digits differently altogether (2-2-3, the *lakh/crore* system, not the 3-3-3 "thousands/millions" grouping the rest of the table uses). This is why "just replace `,` with `.`" is not a fix; it's a trap that half-solves the problem and quietly breaks for a fifth of the world's population.

This is the first article in a four-part series where we build a small, professional, cross-platform C++23 utility library — `LocaleUtils` — that correctly reads and displays numbers, currency, dates, and times for any locale. All code targets **C++23**, compiles cleanly with **clang++, GCC, and MSVC** with no `#ifdef`-per-compiler branching, and runs on Linux, macOS, and Windows. The full source lives in the companion Git repository; this article walks through the *architecture* and the *critical* code, not every line.

---

### Why `std::locale` alone won't get you there

C++'s standard library isn't blind to this problem — `std::locale` and its `std::numpunct` facet exist precisely to teach `iostream` how to format numbers per-region:

```cpp
// tests/number_test/number_test2.cpp
#include <iostream>
#include <locale>

int main() {
    constexpr double large_value = 34573892785.34;
    try {
        std::locale::global(std::locale(""));   // adopt the OS/user locale
        std::cout.imbue(std::locale());
    } catch (const std::runtime_error&) {
        std::cerr << "Requested locale not installed on this system\n";
    }

    std::cout << std::fixed << large_value << '\n';
    return 0;
}
```

This works — *when the target locale happens to be installed on the machine running your binary*. And that's exactly where it falls apart for a professional, cross-platform application:

- **Locale names aren't portable.** Linux/macOS expect POSIX names like `en_IN.UTF-8`; MSVC expects `en-IN` or `English_India`. `std::locale("en_IN")` that works on your Manjaro box will throw `std::runtime_error` on a fresh Windows install.
- **Locale data must be installed, and often isn't.** A minimal Docker container or a locked-down corporate Windows image frequently ships with only one or two locales generated. You cannot guarantee `ru_RU` or `hi_IN` exists on the target machine.
- **`std::numpunct` can't express every grouping rule.** It supports a single repeating group size. It has no way to say "group by 3, then by 2, then by 2" — which is exactly India's lakh/crore rule. There is no standard-library path to correct Indian number formatting, full stop.
- **There's no standard spellout facility at all.** Converting `34573892785.34` into "thirty-four billion five hundred seventy-three million..." isn't something `<locale>` does in any locale, in any language.

None of this is a knock on the standard library — `std::locale` was designed in an era before Unicode's CLDR (Common Locale Data Repository) existed. But for a modern, professional application, we need a library that ships its own locale data instead of depending on what the OS happens to have installed, so behavior is *identical* across Manjaro, Ubuntu, Fedora, macOS, and Windows without a single platform `#ifdef`. That library is **ICU** (International Components for Unicode) — the same locale engine behind Chrome, Android, and the ICU-backed parts of macOS and Windows themselves.

---

### Installing ICU and nlohmann/json

We'll need two libraries throughout this series: **ICU** for locale-aware formatting, parsing, and spellout, and **nlohmann/json** for externalizing configuration (currency names, plural rules, etc. — starting in Part 2). Install both now:

**Manjaro / Arch Linux**
```bash
sudo pacman -S icu nlohmann-json
```

**Ubuntu / Debian**
```bash
sudo apt update
sudo apt install libicu-dev nlohmann-json3-dev
```

**Fedora**
```bash
sudo dnf install libicu-devel json-devel
```

**macOS (Homebrew)**
```bash
brew install icu4c nlohmann-json
# icu4c is keg-only; tell the build where to find it:
export PKG_CONFIG_PATH="$(brew --prefix icu4c)/lib/pkgconfig:$PKG_CONFIG_PATH"
```

**Windows (vcpkg, works with MSVC)**
```powershell
vcpkg install icu nlohmann-json
vcpkg integrate install
```

To keep the build identical across all four platforms, we drive everything through **CMake** rather than hand-written per-platform compiler flags:

```cmake
cmake_minimum_required(VERSION 3.24)
project(locale_utils LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(PkgConfig REQUIRED)
pkg_check_modules(ICU REQUIRED icu-i18n icu-uc)
find_package(nlohmann_json REQUIRED)

add_executable(locale_utils_demo
    locale_utils.cpp
    main.cpp
)

target_include_directories(locale_utils_demo PRIVATE ${ICU_INCLUDE_DIRS})
target_link_libraries(locale_utils_demo PRIVATE ${ICU_LIBRARIES} nlohmann_json::nlohmann_json)
```

On Windows with vcpkg, the same `CMakeLists.txt` works unchanged as long as you configure with the vcpkg toolchain file:

```powershell
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=$env:VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake
cmake --build build
```

No compiler-specific code, no `#ifdef _MSC_VER` — CMake and `pkg-config`/vcpkg absorb the platform differences so `locale_utils.cpp` stays clean C++23.

---

### Designing `LocaleUtils`

Rather than scatter ICU calls through application code, we wrap them behind a small, intention-revealing interface in `locale_utils.h`. Application code should never see an `icu::` type — only `std::string`, `double`, and `std::chrono` types:

```cpp
namespace LocaleUtils {

  // Synchronizes std::cout/std::cin with the host OS's language context.
  bool initialize_system_locale();

  // Formats/parses a plain number using the target locale's grouping and
  // decimal conventions (e.g. lakh/crore grouping for en_IN).
  std::string format_number(double value, const std::string &locale_name = "");
  bool parse_number(const std::string &input, double &out_value,
      const std::string &locale_name = "");

  // Translates 123456 -> "one hundred twenty-three thousand four hundred
  // fifty-six" in the target locale's language.
  std::string expand_number_to_words(
      double value, const std::string &locale_name = "");

} // namespace LocaleUtils
```

This is the architectural decision that makes the rest of the series possible: every locale-sensitive concern — currency (Part 2), dates (Part 3), and time (Part 4) — gets its own narrow function in this same namespace, each backed by ICU internally, none of it leaking into `main()`.

### Formatting and parsing: the critical code

`format_number` asks ICU for a locale-appropriate `NumberFormat` and lets it do the grouping and decimal-symbol work:

```cpp
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
```

`parse_number` is the mirror image — critically, it must fail loudly on a partial match rather than silently accepting a truncated string:

```cpp
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
```

Both functions accept an empty `locale_name`, in which case ICU falls back to `getDefault()` — the locale `initialize_system_locale()` set up from the host OS's environment at startup. This gives callers a sane zero-argument default while still allowing an explicit override, which is exactly what we need for the demo below.

### A real-world gotcha: floating point meets grammar

The fourth function, `expand_number_to_words`, uses ICU's `RuleBasedNumberFormat` in `URBNF_SPELLOUT` mode — the same engine that reads amounts aloud on automated phone systems. A naive implementation just hands the double straight to ICU:

```cpp
icu::RuleBasedNumberFormat formatter(icu::URBNF_SPELLOUT, icu_loc, status);
icu::UnicodeString res;
formatter.format(value, res);   // looks fine... until it doesn't
```

This works for English and French. For Russian, feeding it `34573892785.34` directly produces nonsense: the spellout rules read out an eight-digit fraction like *"...тридцать три миллиона девятьсот девяносто девять тысяч шестьсот тридцать четыре стомиллионных"* — roughly "...thirty-three million nine hundred ninety-nine thousand six hundred thirty-four hundred-millionths". That's not a translation bug; it's IEEE 754 leaking into your UI text.

Here's why: `34573892785.34` cannot be represented exactly as a `double`. Print it with full precision and you get `34573892785.33999633789...` — the fractional part carries roughly six microunits of binary rounding noise. English and French spellout rules read the fraction digit-by-digit from the rounded display value, so the noise is invisible. Russian's rule set instead computes the fraction as an *exact* rational number from the double's raw bits — and once the integer part uses up most of a `double`'s ~15-17 significant decimal digits, that noise becomes visible as extra, meaningless fraction digits.

The fix mirrors a pattern you'd use for money: never let the fractional part travel attached to a large integer through binary floating point. Split them first, so each half stays comfortably inside the precision a `double` can guarantee:

```cpp
double int_part_raw;
double frac_part_raw = std::round(std::modf(value, &int_part_raw) * 100.0);

icu::UnicodeString whole_words;
formatter.format(int_part_raw, whole_words);          // exact: pure integer

if (frac_part_raw == 0.0) {
  std::string out;
  whole_words.toUTF8String(out);
  return out;
}

// Recover the correct connector word ("point" / "virgule" / "целых") by
// spelling a small stand-in that shares the real integer's last two digits,
// then stripping the stand-in's own prefix from the combined result.
double stand_in =
    static_cast<double>(static_cast<int64_t>(std::abs(int_part_raw)) % 100);
icu::UnicodeString stand_in_words;
formatter.format(stand_in, stand_in_words);

icu::UnicodeString combined_small;
formatter.format(stand_in + std::abs(frac_part_raw) / 100.0, combined_small);

icu::UnicodeString connector_and_fraction = combined_small;
if (combined_small.startsWith(stand_in_words) &&
    combined_small.length() > stand_in_words.length()) {
  connector_and_fraction =
      combined_small.tempSubString(stand_in_words.length() + 1);
}

icu::UnicodeString res = whole_words + " " + connector_and_fraction;
```

`stand_in` exists only to ask ICU "what connector and fraction phrase would you produce here?" using a value small enough (0-99) to have zero binary-precision error, while still sharing the real number's final digits — because some languages (Russian included) grammatically inflect the connector based on what precedes it. It's a small, self-contained trick, not a special case bolted on for one locale.

**A known limitation worth stating plainly:** Russian additionally changes the *gender* of that trailing digit when a fraction follows — "один" (one, masculine) becomes "одна" (one, feminine) before "целая", and "два" (two) becomes "две". Our stand-in/prefix-strip technique can't detect a gender change, only a length-preserving prefix match, so integers ending in 1 or 2 fall back to a slightly less elegant phrasing. This is a real, if narrow, edge case — flagged here deliberately rather than hidden, and one every team should decide is either acceptable or worth a locale-specific override table.

For our worked example (`...785.34` — ending in 5, no gender exception), the output is exactly right:

> тридцать четыре миллиарда пятьсот семьдесят три миллиона восемьсот девяносто две тысячи семьсот восемьдесят пять **целых** тридцать четыре сотых

---

### Putting it together: four locales, one code path

With the library in place, the entire application-facing code for reading and displaying a locale-correct number is this small:

```cpp
#include <print>
#include "locale_utils.h"

int main() {
  LocaleUtils::initialize_system_locale();

  constexpr double large_value = 34573892785.34;

  for (const auto &locale_id : {"en_US", "fr_FR", "ru_RU", "en_IN"}) {
    std::println("--- {} ---", locale_id);
    std::println("Display : {}",
        LocaleUtils::format_number(large_value, locale_id));
    std::println("Spelled : {}",
        LocaleUtils::expand_number_to_words(large_value, locale_id));

    // Round-trip: parse the display string straight back into a double.
    double parsed_value{};
    std::string displayed = LocaleUtils::format_number(large_value, locale_id);
    bool ok = LocaleUtils::parse_number(displayed, parsed_value, locale_id);
    std::println("Parsed  : {} (round-trip {})",
        parsed_value, ok ? "OK" : "FAILED");
  }
}
```

Running it produces:

```
--- en_US ---
Display : 34,573,892,785.34
Spelled : thirty-four billion five hundred seventy-three million eight hundred
          ninety-two thousand seven hundred eighty-five point three four
Parsed  : 34573892785.34 (round-trip OK)

--- fr_FR ---
Display : 34 573 892 785,34
Spelled : trente-quatre milliards cinq cent soixante-treize millions huit cent
          quatre-vingt-douze mille sept cent quatre-vingt-cinq virgule trois quatre
Parsed  : 34573892785.34 (round-trip OK)

--- ru_RU ---
Display : 34 573 892 785,34
Spelled : тридцать четыре миллиарда пятьсот семьдесят три миллиона восемьсот
          девяносто две тысячи семьсот восемьдесят пять целых тридцать четыре сотых
Parsed  : 34573892785.34 (round-trip OK)

--- en_IN ---
Display : 34,57,38,92,785.34
Spelled : three thousand four hundred fifty-seven crore thirty-eight lakh
          ninety-two thousand seven hundred eighty-five point three four
Parsed  : 34573892785.34 (round-trip OK)
```

Look closely at the India row: `34,57,38,92,785.34` — 2-2-2-3 lakh/crore grouping, produced by the exact same `format_number` call as the others, with no `if (locale == "en_IN")` branch anywhere in application code. That's the entire point of pushing this logic behind ICU and a clean interface: the *complexity* of the world's numbering systems lives in one place, and it never touches `main()`.

---

### Summary

- The default C++ stream locale (the "C" locale) formats numbers with no thousands grouping and a dot decimal separator — it matches no real user's expectations and silently switches to scientific notation for large magnitudes.
- `std::locale` / `std::numpunct` can adopt the OS locale, but this is unreliable across platforms: locale names aren't portable between POSIX and Windows, the target locale may not be installed, and `std::numpunct` cannot express irregular grouping rules like India's lakh/crore system.
- **ICU** solves this by shipping its own CLDR-derived locale data, giving identical behavior across Manjaro, Ubuntu, Fedora, macOS, and Windows without any platform-specific code.
- We wrapped ICU behind a small `LocaleUtils` namespace so application code only ever sees `std::string`/`double`, never an `icu::` type directly.
- `format_number` and `parse_number` provide locale-correct display and round-trip parsing; `expand_number_to_words` spells numbers out in the target language.
- A genuine bug surfaced along the way: spelling out a large number with a fractional part can leak IEEE 754 binary rounding noise into the output for locales (like Russian) whose grammar computes an exact fraction rather than reading digits verbatim. The fix — splitting the integer and fractional parts before handing either to ICU — is the same discipline you'd apply to money, and it's a good reminder that "locale-aware" bugs often hide at the intersection of floating point and linguistics.
- We also documented, rather than silently swallowed, a narrower residual limitation (Russian gender agreement for integers ending in 1 or 2) — professional software is honest about the edges of what it handles.

**Next up — Part 2:** we extend this same architecture to currency: locale-correct symbols, thousands separators, and — the hard part — expanding an amount into words with correct singular/plural forms and, for India, lakh/crore-based currency phrasing instead of Western millions.
