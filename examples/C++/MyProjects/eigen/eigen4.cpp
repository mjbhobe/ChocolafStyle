// eigen4.cpp - matrix operations (addition, subtraction etc.)
// Compile: clang++ -std=c++23 .... -stdlib=libc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <Eigen/Dense>
#include <iostream>
#include <print>
#include <string>
#include "matprint.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;

int main(void) {
  Eigen::Matrix2d m1, m2; // (2 x 2) matrix of doubles
  m1 << 3, 4, 5, 6;
  m2 << 6, 7, 8, 9;
  std::println("m1:\n{}\nm2:\n{}", m1, m2);

  // add matrices
  Eigen::Matrix2d m3 = m1 + m2;
  std::println("m3 = m1 + m2 ->\n{}", m3);
  // subtract matrices
  m3 = m2 - m1;
  std::println("m3 = m2 - m1 ->\n{}", m3);
  // you also have +=/-= ops
  m3 += m2;
  std::println("m3 += m2 ->\n{}", m3);
  m3 -= m1;
  std::println("m3 -= m1 ->\n{}", m3);

  // addition operator
  return EXIT_SUCCESS;
}
