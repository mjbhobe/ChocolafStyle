// eigen3.cpp - matrix coefficients & attributes
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
  MatrixXd m = MatrixXd::Random(2, 4);

  std::println("Original matrix is a {} rows x {} cols matrix with {} elements", m.rows(), m.cols(), m.size());
  std::cout << "Original Matrix: " << std::endl << m << std::endl;

  // resize matrix [NOTE: resize() method DESTROYS all existing values!!]
  // m.resize(3, 5);
  // use conservativeResize() to resize keeping existing values
  m.conservativeResize(3, 5);
  std::println("Resized matrix is a {} rows x {} cols matrix with {} elements", m.rows(), m.cols(), m.size());
  std::cout << "Resized Matrix (enlarged): " << std::endl << m << std::endl;

  // what happens if I shrink matrix
  m.conservativeResize(1, 3);
  std::println("Resized matrix is a {} rows x {} cols matrix with {} elements", m.rows(), m.cols(), m.size());
  std::cout << "Resized Matrix (shrunk): " << std::endl << m << std::endl;

  Eigen::Matrix2d m2; // (2 x 2) matrix of doubles
  m2 << 3, 4, 5, 6;
  std::println("Matrix2d is a {} rows x {} cols matrix with {} elements", m2.rows(), m2.cols(), m2.size());
  std::cout << "Matrix2d : " << std::endl << m2 << std::endl;

  return EXIT_SUCCESS;
}
