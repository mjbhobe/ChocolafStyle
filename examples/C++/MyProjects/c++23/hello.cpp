#include <cstdio>
#include <print>
#include <string>
#include <utility>

int main(void)
{
  puts("Hello World!");
  // define a pair
  std::pair<std::string, int> pair{"The answer", 42};
  std::println("{} is {}", pair.first, pair.second);
  return 0;
}
