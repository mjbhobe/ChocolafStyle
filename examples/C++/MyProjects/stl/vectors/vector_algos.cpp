// ----------------------------------------------------------------------
// vector_algos.cpp - vectors & STL algorithms
// (NOTE: we use utility functions in stl_utils.h)
//
// illustrates vector functions like sort(), find(), binary_search(),
//  lower_bound(), copy(), reverse() and rotate()
//
// compile: clang++ -std=c++23 -fsanitize=address -fno-omit-frame-pointer ...
// NOTE: on Windows 11 don't use flags other than -std=c++23
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
#include <array>
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


// generates a random integer between lower & upper bounds (both inclusive)
// that is NOT present in vector.
//
int random_int_not_in_vector(const std::vector<int>& vec, int lower, int upper)
{
  // filter out forbidden values (i.e. contents of vec)
  std::vector<int> forbidden_values = vec;
  // remove duplicates from forbidden_values vector above
  std::ranges::sort(forbidden_values);
  auto [ret, last] = std::ranges::unique(forbidden_values);
  forbidden_values.erase(ret, last);


  // now we'll roll-dice & check
  int candidate;
  do {
    candidate = random_int_between(lower, upper);
  } while (std::ranges::binary_search(forbidden_values, candidate));

  return candidate;
}


void sorting_demo()
{
  std::println("Testing std::sort(...) to sort vectors...");

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
  std::cout << people << std::endl;
  // for (const auto &p: people)
  //   std::cout << p << std::endl;
  std::sort(people.begin(), people.end(), compareByName);
  std::cout << "Sorted people vector..." << std::endl;
  std::cout << people << std::endl;
  // for (const auto &p: people)
  //   std::cout << p << std::endl;
}

void searching_demo()
{
  std::println("Testing searching inside std::vector<>(...)");

  // linear search (always guaranteed to find value, if it exists)
  std::vector<int> rand_vec = random_vec<int>(10);
  int index                 = random_int_between(0, 9); // pick a random index
  std::array test_vals = {
    rand_vec.at(index),     // value existing in vector
    random_int_not_in_vector(rand_vec, 50, 100),  // value not existing in vector
  };

  // for linear search we use std::find(vec.begin(), vec.end(), value_to_find);
  for (const auto &val : test_vals) {
    std::println("Try searching for {} in vector {} using std::find(...) [linear search]", val, rand_vec);
    auto it = std::find(rand_vec.begin(), rand_vec.end(), val);
    if (it == rand_vec.end())
      std::cout << "   " << val << " not found!" << std::endl;
    else
      std::cout << "   Found " << val << " at index " << (it - rand_vec.begin()) << std::endl;
  }

  // binary search is much faster for arbit sized vectors, but it requires that
  // vector be sorted, else we get unpredictable results
  std::sort(rand_vec.begin(), rand_vec.end());
  for (const auto &val : test_vals) {
    std::println("Try searching for {} in vector {} using std::binary_search(...) [faster]", val, rand_vec);
    if (std::binary_search(rand_vec.begin(), rand_vec.end(), val))
      std::cout << "Found " << val << std::endl;
    else
      std::cout << "   " << val << " not found!" << std::endl;
  }

  // unfortunately std::binary_search() returns a boolean & does not return a position
  // within the vector where it found the value. To find positions, you should use
  // std::lower_bound() or std::upper_bound() instead.
  // std::lower_bound() returns iterator to first element that is NOT less than
  // the search value (i.e. is >= search_value).
  // NOTE: You must check if iterator holds value searched by you - vector must be sorted
  std::cout << "Using std::lower_bound(...) to search in sorted array & get position..." << std::endl;
  for (const auto &val : test_vals) {
    std::println("Try searching for {} in vector {} using std::lower_bound(...) [get position too]", val, rand_vec);
    auto iter = std::lower_bound(rand_vec.begin(), rand_vec.end(), val);
    if (*iter == val)
        // you must check if iterator holds value searched by you!
        std::cout << "Found " << val << " at position " << (iter - rand_vec.begin()) << std::endl;
    else
        // otherwise std::lower_bound() indicates position where value should be inserted
        // to maintain sorted order
        std::cout << val << " not found!" << std::endl;
  }
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
  sorting_demo();
  searching_demo();
  test_other_algos();

  return EXIT_SUCCESS;
}
