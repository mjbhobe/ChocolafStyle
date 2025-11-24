// ----------------------------------------------------------------------
// vectors1.cpp: basics of std::vector container
// (NOTE: we use utility functions in stl_utils.h)
// compile: clang++ -std=c++23 -fsanitize=address -fno-omit-frame-pointer ...
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
#include <print>
#include <string>
#include <vector>
#include "stl_utils.h"

class Person {
  public:
    Person() = default;
    Person(const std::string &name, int age) : m_name{name}, m_age{age} {}
    // default destructor will do - this is only to illustrate destructor is being called
    ~Person() { std::println("Destructor for {{\"Name: \"{}, \"Age: \"{}}} called!", m_name, m_age); }
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


int main(void)
{
  // declaring & initializing vectors ---------------------------------------
  std::println("// declaring & initializing vectors ---------------------------------------");
  std::vector<int> vec1;                            // create an empty vector
  std::vector<int> vec2(5);                         // vector of 5 integers initialized to 0
  std::vector<int> vec3(5, 10);                     // vector of 5 integers initialized to 10
  std::vector<int> vec4{1, 2, 3, 4, 5, 6, 7, 8, 9}; // std C++ initialization
  // initialize using a generator
  std::vector<int> vec5(10);
  int value = 0;
  // initialize vector with 10 even numbers starting with 2
  std::generate(vec5.begin(), vec5.end(), [&value]() { return value += 2; });
  // you can also copy-initialize a vector, like so
  std::vector<int> vec6(vec5); // initialize vec6 from vec5
  // how about a vector with user-defined class
  std::vector<Person> people = {
      {"Anupa", 49},
      {"Nupoor", 18},
      {"Manish", 56},
      {"Sunila", 83},
  };

  // display vectors
  std::cout << vec2 << std::endl;
  std::cout << vec3 << std::endl;
  std::cout << vec4 << std::endl;
  std::cout << vec5 << std::endl;
  std::cout << vec6 << std::endl;
  std::cout << people << std::endl;
  std::println("***** >>> Person: {}", people.at(2));
  std::println("***** >>> Persons: {}", people);

  // randomly accessing members of class ---------------------------------------
  std::println("\n// randomly accessing members of class ---------------------------------------");
  // using index based access
  // NOTE: index-based access DOES NOT throw an exception for invalid out-of-bound index
  const auto person = people[2];
  std::cout << person << std::endl;
  // what if index goes past # of items?
  // it is best to use the at(..) function to access elements - at() throws exception
  // for out-of-bounds access
  try {
    const auto person2 = people.at(2); // valid index!
    std::cout << person2 << std::endl; // this line will work!
    const auto person7 = people.at(7); // invalid index!
    std::cout << person7 << std::endl; // this line will not execute!!
  }
  catch (const std::exception &e) {
    std::cerr << "Exception " << typeid(e).name() << ": " << e.what() << std::endl;
  }
  // accessing first & last elements
  std::cout << "First person: " << people.front() << " Last person: " << people.back() << std::endl;

  // how many elements in vector? ---------------------------------------
  std::println("\n// how many elements in vector? ---------------------------------------");
  std::println("Vector initialized with generator has {} elements", vec5.size());
  std::println("We have {} people signing up for the Advanced C++ course!", people.size());

  // adding/removing elements from vectors ------------------------------
  std::println("\n// adding/removing elements from vectors ------------------------------");
  std::println("vec4 BEFORE adding elements: {}", vec4);
  // add some elements using push_back
  vec4.push_back(44);
  vec4.push_back(55);
  std::println("vec4 AFTER adding elements: {}", vec4);
  std::println("Adding 66 at 3rd position (i.e vec4[2])");
  vec4.insert(vec4.begin() + 2, 66);
  std::println("vec4 AFTER inserting 66: {}", vec4);
  // using emplace() and emplace_back() avoids un-neccessary copies, especially for
  // user-defined classes
  std::println("Adding {{\"Jagdish\",85}} at end of persons vector using emplace_back()");
  people.emplace_back("Jagdish", 85);
  std::println("Now people vector is: {}", people);
  std::println("Adding {{\"Dattatray\",83}} at 3rd position using emplace()");
  people.emplace(people.begin() + 2, "Dattatray", 83);
  std::println("Now people vector is: {}", people);

  // let's add some more Manish's to the people vector
  people.emplace(people.begin() + 4, "Manish", 65);
  people.emplace(people.begin() + 2, "Manish", 65);
  people.emplace_back("Manish", 45);
  people.emplace_back("Manish", 47);
  std::println("People vector for erase/remove operations:\n{}", people);

  Person to_erase{"Manish", 65};
  std::cout << "Let's try deleting " << to_erase << " from above vector" << std::endl;
  // this statement should remove ALL {"Manish", 65} entries from vector
  people.erase(std::remove(people.begin(), people.end(), to_erase), people.end());
  std::cout << "After delete vector is : " << people << std::endl;
  // now let's try erasing all entries for Manish where age >40 & age<60
  std::println("Erasing all instance of Manish where age >= 40 & <= 60");
  // first let's count
  auto count = std::count_if(people.begin(), people.end(),
      [](const Person &p) { return p.name() == "Manish" && p.age() >= 40 && p.age() <= 60; });
  std::cout << "NOTE: there are " << count << " entries with Manish and age >= 40 && age <= 60" << std::endl;
  auto remove_count = std::erase_if(
      people, [](const Person &p) { return p.name() == "Manish" && p.age() >= 40 && p.age() <= 60; });
  std::cout << "After erasing " << remove_count << " entries, vector is: " << people << std::endl;
  // clear all entries
  std::println("Calling clear() on people collection");
  people.clear();
  // and now add one entry
  people.emplace_back("Emplace Back", 75);


  return EXIT_SUCCESS;
}
