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
  std::string s{"This is a vector"};

  // std::cout << s << ": " << x[0] << ", " << x[1] << ", " << x[2] <<
  // std::endl;
  // std::println("{}: {}", s, std::views::all(vec));
  std::cout << vec << std::endl;
}
