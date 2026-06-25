#include <iostream>
#include <ranges>
#include <string>
#include <vector>

template<typename T>
std::ostream &operator<<(std::ostream &ost, const std::vector<T> &vec)
{
  if (vec.size() <= 0)
    ost << "[]";
  else {
    ost << "[";
    for (auto i = vec.cbegin(); i != vec.cend(); ++i) {
      // display contents of vector as [c1,c2,c3...]
      ost << *i << ((i < vec.cend() - 1) ? "," : "");
    }
    ost << "]";
  }
  return ost;
}


int main()
{
  std::vector<int> vec{1, 2, 3};
  std::string s{"This is a demo of vectors in C++ STL"};

  std::cout << s << std::endl;

  std::cout << "Original vector: " << vec << std::endl;
  // naive way to take sum of all elements
  long sum = 0;
  for (auto e: vec)
    sum += e;
  std::cout << "Sum of all elements: " << sum << std::endl;

  // manipulating all elements of a vector
  // let's say I want to square each element
  for (auto &e: vec)
    e = e * e;
  std::cout << "Squared vector: " << vec << std::endl;

  return EXIT_SUCCESS;
}
