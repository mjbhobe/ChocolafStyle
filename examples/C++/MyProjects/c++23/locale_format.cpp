// ============================================================================
// locale_format.cpp - formatting locale aware numbers, currency, date/time
//
// @author: Manish Bhobe
// My experiments with C/C++, STL, Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// ============================================================================
#include <iomanip>
#include <iostream>
#include <locale>

// for these 3 headers, see note before expand_number_to_words(...) function
#include <unicode/locid.h>
#include <unicode/rbnf.h>
#include <unicode/ustream.h>

// converts a string to proper case, locale aware code
std::string to_proper_case(
    std::string str, const std::locale &loc = std::locale(""))
{
  bool next_should_be_upper = true;

  for (char &c: str) {
    if (std::isspace(c, loc)) {
      next_should_be_upper = true;
    }
    else if (next_should_be_upper) {
      // Use the locale-aware version of toupper
      c = std::toupper(c, loc);
      next_should_be_upper = false;
    }
    else {
      c = std::tolower(c, loc);
    }
  }
  return str;
}

// NOTE: this function REQUIRES icu library to be available on your OS
// On my OS (Manjaro Linux KDE), I installed it using 'sudo pacman -S icu'
// On Windows, you can use vcpkg to install it
std::string expand_number_to_words(
    const double &number, const std::locale &userLocale)
{
  UErrorCode status{U_ZERO_ERROR};
  icu::Locale icuLocale(userLocale.name().c_str());

  // instantiate rules based number formatter
  icu::RuleBasedNumberFormat formatter(icu::URBNF_SPELLOUT, icuLocale, status);
  if (U_FAILURE(status))
    return "FATAL ERROR: ICU Locale Spellout is not available!";

  icu::UnicodeString result;
  formatter.format(number, result);
  std::string out;
  result.toUTF8String(out);
  return to_proper_case(out, userLocale);
}


int main(void)
{
  // get default locale & set it globally
  std::locale userLocale("");
  std::locale::global(userLocale);

  // imbue stdout, stdin, stderr with userLocale
  std::cout.imbue(userLocale);
  std::cin.imbue(userLocale);
  std::cerr.imbue(userLocale);

  // this line prints en_IN on cout
  std::cout << "Your default locale is: " << userLocale.name() << std::endl;

  std::cout << "Localized number formatting..." << std::endl;

  double amount = 12345678.965;

  // NOTE: code below will fail, will display number with exponential notation
  // because std::cout has a default precision limit of 6 significant digits for
  // floating-point numbers. Since your number 12345678.965 requires 11
  // significant digits, std::cout decides that it cannot display it cleanly
  // within 6 digits, abandons fixed-point notation, rounds it, and falls back
  // to scientific notation.

  std::cout << "Number (default): " << amount << std::endl;

  // and this is the fix: use std::fixed & std::setprecision(n) to fix
  std::cout << "Number (locale): " << std::fixed << std::setprecision(3)
            << amount << std::endl;
  // let's expand that to words
  std::cout << "Number (locale) in words: "
            << expand_number_to_words(amount, userLocale) << std::endl;

  // display number as localized currency
  // std::showbase ensures the currency symbol (like ₹, $, or €) is rendered.
  // We multiply by 100 because put_money counts in cents/paise units.
  std::cout << "Currency (std::cout):  " << std::showbase
            << std::put_money(amount * 100.0) << std::endl;


  return EXIT_SUCCESS;
}
