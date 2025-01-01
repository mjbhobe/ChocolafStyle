// templ1.cpp - containers & iterators
// Compile: g++/clang++ -std=c++23 .... -lstdc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <print> // for std::println()
#include <typeinfo>
#include <vector>

int main(void)
{
  std::vector<int> x_vals{10, 20, 30, 40, 50, 60, 70, 80, 90, 100};

  // iterate over vector using [] - index accessor
  for (int i = 0; i < x_vals.size(); ++i)
    std::print("{} ", x_vals[i]);
  std::println("");

  // iterate over vector using at() call
  for (int i = 0; i < x_vals.size(); ++i)
    std::print("{} ", x_vals.at(i));
  std::println("");

  // using iterators
  std::vector<long long> y_vals{10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
  for (auto it = y_vals.cbegin(); it != y_vals.cend(); ++it)
    std::print("{} ", *it);
  std::println("");
  std::println("Typeof iterator: {}", typeid(y_vals.begin()).name());
  std::println("Typeof const iterator: {}", typeid(y_vals.cbegin()).name());

  // using new syntax
  for (auto v : y_vals)
    std::print("{} ", v);
  std::println("");

  // reverse iteration
  for (auto it = y_vals.crbegin(); it != y_vals.crend(); ++it)
    std::print("{} ", *it);
  std::println("");

  // modify inplace
  for (auto it = y_vals.begin(); it != y_vals.end(); ++it)
    *it /= 5.0;

  std::println("y_vals with each element divided by 5");
  for (auto v : y_vals)
    std::print("{} ", v);
  std::println("");

  return EXIT_SUCCESS;
}
