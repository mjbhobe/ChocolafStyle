// eigen2.cpp - matrices & vectors
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

using Eigen::MatrixXd;
using Eigen::VectorXd;

int main(void) {
  // create a 3 x 3 matrix of random numbers
  MatrixXd m = MatrixXd::Random(3, 3);

  std::cout << "Original Matrix: " << std::endl << m << std::endl;
  // std::println("Original Matrix:\n {}\n", m);

 // add a constant matrix (3x3 matrix with all 1.2s)
  MatrixXd c = MatrixXd::Constant(3, 3, 1.2);
  std::cout << std::endl << "Constant Matrix: " << std::endl << c << std::endl;

  m = m + c;
  std::cout << std::endl << "Original Matrix  + Constant(3, 3, 1.2): " << std::endl << m << std::endl;

  // m = (m + c) * 50
  m = m * 50;
  std::cout << std::endl << "(Original Matrix  + Constant(3, 3, 1.2)) * 50: " << std::endl << m << std::endl;

  // create a vector
  VectorXd v(3);
  v << 1, 2, 3;
  std::cout << std::endl << "Vector: " << std::endl << v << std::endl;

  // m * v
  // std::cout << std::endl << "m * v: " << std::endl << (m * v) << std::endl;
  std::println("m * v: {}", (m * v));


  return EXIT_SUCCESS;
}
