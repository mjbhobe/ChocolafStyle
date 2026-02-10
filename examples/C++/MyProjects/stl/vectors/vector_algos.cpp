// ----------------------------------------------------------------------
// vector_algos.cpp - vectors & STL algorithms
// (NOTE: we use utility functions in stl_utils.h)
// compile: clang++ -std=c++23 -fsanitize=address -fno-omit-frame-pointer ...
// ----------------------------------------------------------------------
//
// @Author: Manish Bhobe
// Code shared for learning purposes only! Use at your own risk
// ----------------------------------------------------------------------

// required a c++23 compiler!
#if __cplusplus < 202302L && (!defined(_MSVC_LANG) || _MSVC_LANG < 202004L)
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++/cl use -std=c++23 or /std:c++23)
#endif

#include <algorithm>
#include <iostream>
#include <iterator>
#include <print>
#include <string>
#include <vector>
#include "stl_utils.h"

class Person {
  public:
    std::string name;
    int age{0};

    Person(std::string n, int a) : name{n}, age{a} {}
    friend std::ostream &operator<<(std::ostream &ost, const Person &p)
    {
      ost << p.name << " (" << p.age << ")";
      return ost;
    }
};


void sorting_demo()
{
  // create an initial vector of 10 random integers (between 0 & 100)
  std::vector<int> rand_vec = random_vec<int>(10);
  std::println("Initial vector: {}", rand_vec);

  // sorting vector (by default ascending)
  std::sort(std::begin(rand_vec), std::end(rand_vec));
  std::println("Sorted vector: {}", rand_vec);
  // and sort in descending order
  std::sort(std::begin(rand_vec), std::end(rand_vec), std::greater<>());
  std::println("Sorted vector (desc): {}", rand_vec);

  // sort vector with custom data-type
  std::vector<Person> people = {
      Person("Regan", 30),
      Person("Regan", 25),
      Person("Lisa", 40),
      Person("Corbin", 45),
  };
  // lambda for sorting: sort by names ascending; if names equal, sort by age ascending
  auto compareByName = [](const Person &a, const Person &b) -> bool {
    return (a.name == b.name ? a.age < b.age : a.name < b.name);
    // return a.name < b.name;
  };
  std::cout << "Initial people vector..." << std::endl;
  for (const auto &p: people)
    std::cout << p << std::endl;
  std::sort(people.begin(), people.end(), compareByName);
  std::cout << "Sorted people vector..." << std::endl;
  for (const auto &p: people)
    std::cout << p << std::endl;
}

void searching_demo()
{
  // linear search (always guaranteed to find value, if it exists)
  std::vector<int> rand_vec = random_vec<int>(10);
  int index                 = random_int_between(0, 9); // pick a random index
  int val                   = rand_vec.at(index);

  // for linear search we use std::find(vec.begin(), vec.end(), value_to_find);
  std::println("Try searching for {} in vector {}", val, rand_vec);
  auto it = std::find(rand_vec.begin(), rand_vec.end(), val);
  if (it == rand_vec.end())
    std::cout << "   " << val << " not found!" << std::endl;
  else
    std::cout << "   Found " << val << " at index " << (it - rand_vec.begin()) << std::endl;

  // binary search is much faster for arbit sized vectors, but it requires that
  // vector be sorted, else we get unpredictable results
  std::sort(rand_vec.begin(), rand_vec.end());
  if (std::binary_search(rand_vec.begin(), rand_vec.end(), val))
    std::cout << "Found " << val << std::endl;
  else
    std::cout << "   " << val << " not found!" << std::endl;

  // unfortunately std::binary_search() returns a boolean & does not return a position
  // within the vector where it found the value. To find positions, you should use
  // std::lower_bound() or std::upper_bound() instead.
  // std::lower_bound() returns iterator to first element that is NOT less than
  // the search value (i.e. is >= search_value).
  // NOTE: You must check if iterator holds value searched by you - vector must be sorted
  std::cout << "Using std::lower(...) to search in sorted array..." << std::endl;
  auto iter = std::lower_bound(rand_vec.begin(), rand_vec.end(), val);
  if (*iter == val)
    // you must check if iterator holds value searched by you!
    std::cout << "Found " << val << " at position " << (iter - rand_vec.begin()) << std::endl;
  else
    // otherwise std::lower_bound() indicates position where value should be inserted
    // to maintain sorted order
    std::cout << val << " not found!" << std::endl;
}

void test_other_algos()
{
  // copying vectors
  std::println("Testing std::copy(...)");
  std::vector<int> rand_vec = random_vec<int>(10);
  std::vector<int> vec2(rand_vec.capacity());
  // now copy rand_vec to vec2
  std::copy(rand_vec.begin(), rand_vec.end(), vec2.begin());
  std::println("  - Source vector: {}", rand_vec);
  std::println("  - Copied vector: {}", vec2);

  // reversing vector
  std::println("Testing std::reverse(...)");
  std::println("  - Source vector: {}", vec2);
  std::reverse(vec2.begin(), vec2.end());
  std::println("  - After reversing: {}", vec2);

  // rotating vector
  std::println("Testing std::rotate(...)");
  std::vector<int> vec3(rand_vec.capacity());
  std::copy(rand_vec.begin(), rand_vec.end(), vec3.begin());
  std::println("  - Source vector: {}", vec3);
  // now rotate
  std::rotate(vec3.begin(), vec3.begin() + 4, vec3.end());
  std::println("  - Rotated vector: {}", vec3);
}


int main(void)
{
  // sorting_demo();
  // searching_demo();
  test_other_algos();

  return EXIT_SUCCESS;
}
