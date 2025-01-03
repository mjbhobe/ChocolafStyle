// --------------------------------------------------------
// main.cpp - main() - starter function
// --------------------------------------------------------

// require C++ 23
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler!
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <cstdint>
#include <format>
#include <ostream>
#include <print>
#include <string>
#include <utility>
#include <vector>
#include "Image.h"


int main(void)
{
  Image im0{};
  std::println("im0: {} - after ctor", im0);
  Image im1{100, 200};
  std::println("im1: {} - after ctor", im1);
  Image im2{300, 400};
  std::println("im2: {} - after ctor", im2);

  return EXIT_SUCCESS;
}
