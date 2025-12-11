// ----------------------------------------------------------------------
// vector_mem.cpp - vectors & memory management
// (NOTE: we use utility functions in stl_utils.h)
// compile: clang++ -std=c++23 -fsanitize=address -fno-omit-frame-pointer ...
// ----------------------------------------------------------------------
//
// @Author: Manish Bhobe
// Code shared for learning purposes only! Use at your own risk
// ----------------------------------------------------------------------

// required a c++23 compiler!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <algorithm>
#include <chrono>
#include <iostream>
#include <iterator>
#include <mutex>
#include <print>
#include <string>
#include <thread>
#include <vector>
#include "stl_utils.h"

void size_and_capacity()
{
  std::vector<int> myVec;

  // check size & capacity before doing anything
  std::println("Initial size: {} - initial capacity: {}", myVec.size(), myVec.capacity());

  // add 10 items & keep checking size & capacity after each add
  for (auto i = 0; i < 10; i++) {
    myVec.push_back(i);
    std::println("After adding {} -> size: {} - capacity: {}", i, myVec.size(), myVec.capacity());
  }

  // resize vector & check size & capacity
  myVec.resize(5);
  std::println("\nAfter resize(5) -> size: {} - capacity: {}", myVec.size(), myVec.capacity());

  // shrink to fit & check
  myVec.shrink_to_fit();
  std::println("\nAfter shrink_to_fit() -> size: {} - capacity: {}", myVec.size(), myVec.capacity());

  // add one more element & check
  myVec.push_back(44);
  std::println("\nAfter adding 1 more elem -> size: {} - capacity: {}", myVec.size(), myVec.capacity());
}

void test_reserve()
{
  // illustrates how reserving memory up-front can speed up large inserts into vector
  constexpr size_t num_elems = 100'000;

  // try adding without reserve
  std::vector<int> vec1;
  auto start = std::chrono::high_resolution_clock::now();
  for (auto i = 0; i < num_elems; i++)
    vec1.push_back(i);
  auto end                              = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> elapse1 = end - start;
  std::println("\nWithout reserve operation took {} seconds", elapse1.count());


  // now try adding with reserve
  std::vector<int> vec2;
  vec2.reserve(num_elems);
  auto start2 = std::chrono::high_resolution_clock::now();
  for (auto i = 0; i < num_elems; i++)
    vec2.push_back(i);
  auto end2                             = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double> elapse2 = end2 - start2;
  std::println("\nWith reserve operation took {} seconds", elapse2.count());
  std::println("\nIt took {} seconds less than befors", elapse1.count() - elapse2.count());
}

int main(void)
{
  // show size & capacity usage
  size_and_capacity();
  // test how reserve saves time
  test_reserve();

  return EXIT_SUCCESS;
}
