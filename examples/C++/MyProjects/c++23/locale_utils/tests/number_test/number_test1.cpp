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

#include <iostream>

int main(void)
{
  constexpr double large_value = 34573892785.34;
  std::cout << "Value: " << large_value << '\n';

  std::cout << "Enter a number: ";
  double user_value{};
  std::cin >> user_value;
  std::cout << "You entered: " << user_value << '\n';
  return 0;
}
