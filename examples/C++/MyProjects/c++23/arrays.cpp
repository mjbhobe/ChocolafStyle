// =========================================================================
// arrays.cpp: working with STL arrays
//
// @author: Manish Bhobe
// My experiments with C/C++, STL and Qt Framework
// Code shared for learning purposes only! Use at your own risk.
// =========================================================================

#include <array>
#include <print>

int main(void)
{
  // NOTE: you MUST know the size of your array at compile time!
  const std::array<int, 6> ints{1, 2, 3, 4, 5, 6};
  std::println("Array has {} elements", ints.size());
  std::println(
      "First element is {}, Last element is {}", ints.front(), ints.back());
  // NOTE: arrays also provides arr[i] subscript to access the ith element
  // There is NO index range checking if you use this notation. arr.at(i) checks
  // bounds hence preferred over arr[i]!
  std::println(
      "Element at index {} is {}", ints.size() / 2, ints.at(ints.size() / 2));
  // this line will fail
  std::println("This line won't print: {}", ints.at(ints.size()));
  return 0;
}
