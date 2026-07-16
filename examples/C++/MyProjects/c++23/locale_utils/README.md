# LocaleUtils

A small C++23 library that wraps ICU to provide locale-aware number, currency,
and date/time formatting and parsing, plus "spelled out in words" number and
currency expansion (e.g. `123456` -> `"one hundred twenty-three thousand four
hundred fifty-six"`). Currency word expansion is driven by a JSON profile
(`locales_config.json`) that supplies per-locale unit names (e.g. "dollar" /
"cents", "rupee" / "paise").

## Functions

| Function | Description |
|---|---|
| `initialize_system_locale()` | Synchronizes `std::cout`/`std::cin`/`std::cerr` with the host OS locale. |
| `format_number(value, locale)` | Formats a number with locale-aware grouping/decimal separators. |
| `parse_number(input, out_value, locale)` | Parses a locale-formatted number string into a `double`. |
| `format_currency(value, locale)` | Formats a value as a locale-aware currency string. |
| `parse_currency(input, out_value, locale)` | Parses a locale-formatted currency string into a `double`. |
| `format_date_time(tp, date_only, locale)` | Formats a `chrono::system_clock::time_point` using the locale's medium date/time layout. |
| `format_short_date_time(tp, locale)` | Formats a time point using the locale's short layout (e.g. `MM/DD/YY`). |
| `parse_date(input, out_time, locale)` | Parses a locale-formatted date string into a time point. |
| `parse_date_time(input, out_time, locale)` | Parses a locale-formatted date+time string into a time point. |
| `expand_number_to_words(value, locale)` | Spells out a number in words for the given locale. |
| `expand_currency_to_words(amount, locale)` | Spells out a currency amount in words (major + minor units), using `locales_config.json` for unit names. |

An empty `locale` argument uses the process's default ICU locale.

## Build & Install

Requires a C++23 compiler, [ICU](https://icu.unicode.org/), and
[nlohmann-json](https://github.com/nlohmann/json). Produces a shared library
(`locale_utils`), installs the public header, and installs
`locales_config.json` to a location the library finds automatically at
runtime — no need to run the library from this source folder.

### Linux (Ubuntu / Manjaro / Fedora)

Install dependencies:

```bash
# Ubuntu/Debian
sudo apt install libicu-dev nlohmann-json3-dev cmake ninja-build

# Manjaro/Arch
sudo pacman -S icu nlohmann-json cmake ninja

# Fedora
sudo dnf install libicu-devel json-devel cmake ninja-build
```

Build and install:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build
sudo cmake --install build
```

By default this installs under `/usr/local` (library in `lib`/`lib64`,
header in `include`, `locales_config.json` in `share/locale_utils`). Pass
`-DCMAKE_INSTALL_PREFIX=/usr` to install into `/usr` instead.

### macOS

Install dependencies (via [Homebrew](https://brew.sh/)):

```bash
brew install icu4c nlohmann-json cmake ninja
```

Build and install:

```bash
cmake -S . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="$(brew --prefix icu4c)"
cmake --build build
sudo cmake --install build
```

### Windows

Install dependencies via [vcpkg](https://vcpkg.io/):

```powershell
vcpkg install icu nlohmann-json
```

Build and install:

```powershell
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE="<vcpkg-root>/scripts/buildsystems/vcpkg.cmake"
cmake --build build --config Release
cmake --install build --config Release
```

Windows has no system-wide "install location" convention, so
`locale_utils.dll` locates `locales_config.json` relative to its own path at
runtime instead of a baked-in path: either next to the DLL, or in
`..\share\locale_utils\` relative to it (matching the `bin`/`share` layout
`cmake --install` produces). For a simple xcopy-style deployment, just keep
`locales_config.json` next to `locale_utils.dll`.

### Overriding the config file location

On any OS, set the `LOCALE_UTILS_CONFIG` environment variable to an absolute
path to use a specific `locales_config.json`, bypassing the search above.
