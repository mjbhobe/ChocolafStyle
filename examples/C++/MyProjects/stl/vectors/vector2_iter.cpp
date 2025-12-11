// ----------------------------------------------------------------------
// vector2_iter.cpp - using iterators with std::vector
// (NOTE: we use utility functions in stl_utils.h)
// compile: clang++ -std=c++23 -fsanitize=address -fno-omit-frame-pointer ...
//
// ----------------------------------------------------------------------
// iterators are used to traverse, access & potentially modify the
// elements in the vector
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
#include <mutex>
#include <print>
#include <string>
#include <thread>
#include <vector>
#include "stl_utils.h"

// global mutex
std::mutex vecMutex;

class Person {
  public:
    Person() = default;
    Person(const std::string &name, int age) : m_name{name}, m_age{age} {}
    ~Person() = default;
    // helper function to display name to std::ostream&
    friend std::ostream &operator<<(std::ostream &ost, const Person &person)
    {
      ost << "{\"Name\": " << person.m_name << ", \"Age\": " << person.m_age << "}";
      return ost;
    }
    // comparison function
    bool operator==(const Person &other) { return (m_name == other.name()) && (m_age == other.age()); }

    // member accessors
    const std::string &name() const { return m_name; }
    int age() const { return m_age; }
    // member modifiers
    void setName(const std::string &newName) { m_name = newName; }
    void setAge(int newAge) { m_age = newAge; } // ignoring checks for now
  private:
    std::string m_name;
    int m_age{0};
};

template<typename CharT>
struct std::formatter<Person, CharT> {

    constexpr auto parse(std::basic_format_parse_context<CharT> &ctx) { return ctx.begin(); }

    template<typename FormatContext>
    auto format(const Person &person, FormatContext &ctx) const
    {
      return std::format_to(ctx.out(), "{{\"Name\": {}, \"Age\": {}}}", person.name(), person.age());
    }
};

void add_to_vector(std::vector<Person> &people, int how_many)
{
  // lock vector (flip mutex) a long as I am inserting into it
  std::lock_guard<std::mutex> guard(vecMutex);
  std::vector<std::string> names{"Anupa", "Nupoor", "Manish", "Sunila", "Jagdish"};

  // let's create 'how_many' random entries and append to people vector
  // using a back_inserter (or output iterator)
  std::generate_n(std::back_inserter(people), how_many, [&]() mutable {
    std::string name = random_pick_from_vector(names);
    size_t age       = random_int(10, 100);
    return Person(name, age);
  });
}

void print_vector(const std::vector<Person> &v, const std::string &prompt = "")
{
  // lock vector (flip mutex) as long as I am printing vector
  // (so no other thread can modify vector while I am printing it!)
  std::lock_guard<std::mutex> guard(vecMutex);
  std::println("{} {}", prompt, v);
}


int main(void)
{
  // we will use our vector of Person(s) in this example
  std::vector<std::string> names{"Anupa", "Nupoor", "Manish", "Sunila", "Jagdish"};
  std::vector<Person> people{};

  // let's create 20 random entries into people vector
  // using a back_inserter (or output iterator)
  std::generate_n(std::back_inserter(people), 20, [&]() mutable {
    std::string name = random_pick_from_vector(names);
    size_t age       = random_int(10, 100);
    return Person(name, age);
  });

  // std::println("Original vector:\n{}", people);
  std::println("\nTraversing vector with iterators (classic method)...");
  // classic way of traversing vectors
  std::cout << "[" << std::endl;
  for (auto iter = people.begin(); iter != people.end(); ++iter)
    std::cout << "   " << *iter << ", " << std::endl;
  std::cout << "]" << std::endl;

  std::println("\nUsing random access iterators....");
  std::vector<Person> people2{};
  std::thread t1(add_to_vector, std::ref(people2), 15);
  t1.join(); // kick off
  std::thread t2(print_vector, std::ref(people2), "Contents of vector:\n");
  t2.join();


  std::println("\nUsing range based loops for iterations....");
  std::println("[");
  for (const Person &person: people)
    std::println("   {},", person);
  std::println("]");

  // you can also use range-based loops to modify values
  for (Person &p: people)
    p.setAge(p.age() / 2);
  // now let's display last 5
  std::println("Displaying last 5 entries after halving age");
  std::println("[");
  for (auto iter = people.end() - 5; iter != people.end(); ++iter)
    std::cout << "   " << *iter << ", " << std::endl;
  std::println("]");


  return EXIT_SUCCESS;
}
