// vec1.cpp - introducting std::vectors
// to compile: clang++ ... -std=c++23 vec1.cpp -o vec1 -stdlib=libc++
#include <iostream>
#include <print>
#include <sstream>
#include <string>
#include <vector>

template<typename T>
std::string vec2str(const std::vector<T> &vec) {
  std::ostringstream oss;
  oss << "[";
  for (size_t i = 0; i < vec.size(); ++i) {
    oss << vec[i];
    if (i < vec.size() - 1)
      oss << ", ";
  }
  oss << "]";
  return oss.str();
}

// Generic operator<< for any std::vector<T>
template<typename T>
std::ostream &operator<<(std::ostream &os, const std::vector<T> &vec) {
  os << "[";
  for (std::size_t i = 0; i < vec.size(); ++i) {
    os << vec[i];
    if (i + 1 != vec.size())
      os << ", ";
  }
  os << "]";
  return os;
}

int main(void) {
  std::vector<int> vec1{2, 4, 6, 8, 10};

  std::println("Vector: {}", vec2str(vec1));
  // will call ostream << operator function
  std::cout << vec1 << std::endl;

  return EXIT_SUCCESS;
}
