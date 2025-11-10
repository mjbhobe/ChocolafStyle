// eigen1.cpp - getting started with the Eigen C++ library
// Compile: clang++ -std=c++23 .... -stdlib=libc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <Eigen/Dense>
#include <iostream>
#include <string>

using Eigen::MatrixXd;

int main(void) {
  MatrixXd m(2, 2);
  m(0, 0) = 3;
  m(1, 0) = 2.5;
  m(0, 1) = -1;
  m(1, 1) = m(1, 0) + m(0, 1);

  // std::println("Matrix: {}", m);
  std::cout << "Matrix: " << m << std::endl;

  return EXIT_SUCCESS;
}
