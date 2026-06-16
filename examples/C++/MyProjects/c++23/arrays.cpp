#include <array>
#include <print>

int main(void)
{
  // NOTE: you MUST know the size of your array at compile time!
  const std::array<int, 6> ints{1, 2, 3, 4, 5, 6};
  std::println("Array has {} elements", ints.size());
  std::println("First element is {}, Last element is {}", ints.front(), ints.back());
  std::println("Array at index {} is {}", ints.size() / 2, ints.at(ints.size() / 2));
  return 0;
}
