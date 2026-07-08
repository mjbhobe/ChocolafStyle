// =========================================================================
// number_test2.cpp - basic reading/writing of large numbers
//   in standard C++ with std::locale
//
// Compile: clang++ -std=c++23 number_test1.cpp -o number_test1 -lstdc++
//
// Author: Manish Bhobe
// My experiments with C/C++, STL and Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// =========================================================================

#include <iostream>
#include <iomanip>
#include <locale>
#include <print>    // C++23 

int main(void)
{
  constexpr double large_value = 34573892785.34;

  try {
    // adopt user's default locale settings
    std::locale::global(std::locale(""));
    std::cout.imbue(std::locale());
  }
  catch (const std::runtime_error &err) {
    std::cerr << "Requested locale not installed on system!\n";
  }

  std::cout << std::fixed << std::setprecision(3) << large_value << "\n";
  // or with C++23 compiler you can use the following code
  // NOTE: the L in the {:.3Lf} specifier! If you use
  // just {:.3f} it will default to "C" locale even when you
  // have std::locale::global(std::locale("")) in your code
  std::println("Value: {:.3Lf}", large_value);
  return 0;
}
