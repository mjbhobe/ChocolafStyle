#include <boost/multiprecision/cpp_int.hpp>
#include <iostream>
#include <print>
using namespace boost::multiprecision;

cpp_int factorial(cpp_int num)
{
  cpp_int fact{1};

  for (cpp_int i = num; i > 1; --i)
    fact *= i;
  return fact;
}


int main(void)
{
  cpp_int num{};

  while (num != -1) {
    std::cout << "Number (-1 to quit)? ";
    std::cin >> num;
    if (num == -1)
      break;
    std::cout << num << "! = " << factorial(num) << std::endl;
  }
}
