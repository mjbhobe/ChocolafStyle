// =========================================================================
// number_test1.cpp - basic reading/writing of large numbers
//   in standard C++
//
// Compile: clang++ -std=c++23 number_test1.cpp -o number_test1 -lstdc++
//
// Author: Manish Bhobe
// My experiments with C/C++, STL and Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// =========================================================================

#if defined(_MSC_VER)
  #if !defined(_MSVC_LANG) || _MSVC_LANG < 202302L
    #error "This file requires C++23 or later. Compile with /std:c++latest (MSVC)."
  #endif
#elif defined(__clang__) || defined(__GNUC__)
  #if __cplusplus < 202302L
    #error "This file requires C++23 or later. Compile with -std=c++23 (clang++/g++)."
  #endif
#endif

#include <cstdio>
#include <iostream>
#include <print>

int main(void)
{
  constexpr double large_value = 34573892785.34;
  std::cout << "Value: " << large_value << '\n';

  std::cout << "Enter a number: ";
  double user_value{};
  ::fflush(stdin);
  std::cin >> user_value;
  std::cout << "You entered: " << user_value << '\n';
  // check what println prints for large numbers (C++23 feature)
  std::println("You entered (println): {}", user_value);
  return 0;
}
