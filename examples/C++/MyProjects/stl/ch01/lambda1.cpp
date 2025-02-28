// lambda1.cpp : illustrating Lambda expressions in C++23
// compile: clang++ -std=c++23 lambda1.cpp -stdlib=libc++

// require C++ 23 compiler!!
#if __cplusplus < 202302L
#error This code requirers a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <cmath>
#include <functional>
#include <print>
#include <vector>

// clang-format off
namespace {
  std::vector<int> s_ValuesInt{
    1, 4, 7, 9, 12, 13, 15, 22, 27, 33, 38, 44, 51,
    58, 63, 68, 71, 77, 82, 87, 93, 95, 98, 99
  };
  std::vector<double> s_ValuesDouble{
    10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0
  };
} // namespace

// clang-format on

void sum_evens()
{
  // use lambda expression to sum even numbers
  // in a vector of ints
  std::vector<int> vec1{s_ValuesInt}; // make a copy

  auto is_even = [](int x) { return x % 2 == 0; };
  auto sum{0};

  // walk element by element
  for (auto x : vec1) {
    if (is_even(x))
      sum += x;
  }
  std::println("sum_evens = {}", sum);
}

auto sum_if(const std::vector<int>& vec, const std::function<bool(int)>& predicate)
{
  // use a function like bool fxn(int) to determine condition
  // pick number in vector & then sum it
  int sum{0};

  for (auto x : vec) {
    if (predicate(x)) {
      sum += x;
    }
  }
  return sum;
}

void use_capture()
{
  double cap_val{2.0};
  std::vector<double> vec1{s_ValuesDouble};

  // use captured value in calculations
  auto calc1 = [cap_val](double x) { return std::sqrt(x) + cap_val; };

  for (auto x : vec1) {
    auto y = calc1(x);
    std::println("x: {:.2f}, y: {:.4f}", x, y);
  }
}

int main(void)
{
  sum_evens();

  // use sum_if to sum all multiples of 3
  auto sum_multiple3_fxn = [](int x) -> bool { return x % 3 == 0; };
  auto sum3{0};
  sum3 = sum_if(s_ValuesInt, sum_multiple3_fxn);
  std::println("Sum_if (multiples of 3) = {}", sum3);

  // lambda with external value passed in
  std::println("Using external values with lambda...");
  use_capture();
}
