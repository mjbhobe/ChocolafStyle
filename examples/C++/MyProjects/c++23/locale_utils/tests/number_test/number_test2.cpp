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
#include <locale>

int main(void)
{
  constexpr double large_value = 34573892785.34;

  try {
    // adopt OS/user's locale, instead of default "C" locale
    std::locale::global(std::locale(""));
    std::cout.imbue(std::locale());
    std::cin.imbue(std::locale());
  }
  catch (const std::runtime_error &err) {
    std::cerr << "Requested locale not installed on system!\n";
  }

  std::cout << std::fixed << large_value << "\n";
  return 0;
}
