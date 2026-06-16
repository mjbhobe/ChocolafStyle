// vec.cpp - using vectors
#include <iostream>
#include <print>
#include <vector>

template<typename T>
std::ostream &operator<<(std::ostream &ost, const std::vector<T> &vec)
{
  ost << "[";
  for (auto elem: vec)
    ost << elem << ",";
  ost << "]";
  return ost;
}


int main(void)
{
  std::vector<int> vec{1, 2, 3, 4, 5, 6};
  std::cout << vec << std::endl;
  return 0;
}
