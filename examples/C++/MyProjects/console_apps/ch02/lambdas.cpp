#include <algorithm>
#include <iostream>
#include <vector>

int main(void)
{
  std::vector v{2, 3, 7, 14, 23};
  // ex1: simple lambda: just show the values
  std::for_each(v.begin(), v.end(), [](int x) { std::cout << x << " "; });
  std::cout << std::endl;

  // ex2: check if member of vector is even or not
  std::for_each(v.begin(), v.end(), [](int x) {
    if (x % 2 == 0) {
      std::cout << x << " is even" << std::endl;
    }
    else {
      std::cout << x << " is odd" << std::endl;
    }
  });

  // ex3: but what if we want to check if each number is divisible by some number
  int d = 3;
  std::for_each(v.begin(), v.end(), [d](int x) {
    if (x % d == 0) {
      std::cout << x << " is divisible by " << d << std::endl;
    }
    else {
      std::cout << x << " is not divisible by " << d << std::endl;
    }
  });
  return 0;
}
