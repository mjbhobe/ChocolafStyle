// display floating point with multiple precisions
//
// to compile: g++ -std=c++23 ... -stdlib=libc++

#include <stdlib.h>
#include <iostream>
#include <iomanip>
#include <cmath>

int main(void) {
  const float num{11.55};
  double root = sqrt(num);

  std::println("Square root of {:.2f} with various precisions", num);
  std::println("");

  for(auto p=0; p<=8; ++p) {
    std::cout << std::setprecision(p) << root << std::endl;
  }

  return EXIT_SUCCESS;
}



