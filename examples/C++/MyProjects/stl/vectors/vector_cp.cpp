// ----------------------------------------------------------------------
// vector_cp.cpp - using comparators & predicates with std::vector
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
    Person(std::string n, int a, double s) : m_name{n}, m_age{a}, m_salary{s} {}
    friend std::ostream &operator<<(std::ostream &ost, const Person &p)
    {
      std::string s = std::format("{} ({} ${:.2f})", p.m_name, p.m_age, p.m_salary);
      //ost << p.name << " (" << p.age << " " ")";
      ost << s;
      return ost;
    }

    // member accessors
    const std::string &name() const { return m_name; }
    int age() const { return m_age; }
    double salary() const { return m_salary;}
    // member modifiers
    void setName(const std::string &newName) { m_name = newName; }
    void setAge(int newAge) { m_age = newAge; } // ignoring checks for now
    void setSalary(double newSal) { m_salary = newSal; } // ignoring checks for now
  private:
    std::string m_name;
    int m_age{0};
    double m_salary{0.0f};
};

template<typename CharT>
struct std::formatter<Person, CharT> {

  constexpr auto parse(std::basic_format_parse_context<CharT> &ctx) { return ctx.begin(); }

  template<typename FormatContext>
  auto format(const Person &person, FormatContext &ctx) const
  {
    return std::format_to(ctx.out(), "{{\"Name\": {}, \"Age\": {}, \"Salary\": {.2f}}}",
      person.name(), person.age(), p.salary());
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


/*
 * A comparator is essentially a callable object that returns a bool. It’s used to
 * dictate the order of elements, especially in sorting or searching operations.
 * By default, operations such as std::sort use the (<) operator to compare elements,
 * but using a comparator we can change that. This is especially useful when you want
 * to sort custom C++ classes, like our Person Class above
 */
void comparator_demo()
{
  // generate a vector of 10 Person Objects
  std::vector<std::string> names{
    "Anupa", "Nupoor", "Manish", "Sunila", "Jagdish",
    "Dattatray", "Ameeta", "Aditya", "Sanjivi", "Aashka",
    "Aarti", "Atool", "Awani", "Aadnya"
  };
  std::vector<Person> people{};

  // let's create 15 random entries into people vector
  // using a back_inserter (or output iterator)
  std::generate_n(std::back_inserter(people), 20, [&]() mutable {
    std::string name = random_pick_from_vector(names);
    size_t age       = random_int_between(10, 90);
    double sal       = random_float_between(25'000.0, 5'50'000.0);
    return Person(name, age, sal);
  });

  std::println("Original vector: {}", people);

}

int main(void)
{
  comparator_demo();
  return EXIT_SUCCESS;
}