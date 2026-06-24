// ------------------------------------------------------------------------------
// Hello.cpp - cannonical Hello World!
// compile:
//   (On Windows) clang++ -std=c++23 Hello.cpp -o Hello -stdlib=libc++
//   (On Max/*nix) clang++ -std=c++23 Hello.cpp -o Hello -lstdc++
//
// @author: Manish Bhobe
// My experiments with C/C++/STL and Qt. Code shared for learning purposed only!
// ------------------------------------------------------------------------------
#include <print>

int main(void)
{
  // NOTE: std::println() will work with C++ 23 compiler ONLY!
  std::println("Hello World!\n");
  return EXIT_SUCCESS;
}
