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
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
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
  auto compareByName = [](const Person &a, const Person &b) {
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


int main(void)
{
  sorting_demo();

  return EXIT_SUCCESS;
}
