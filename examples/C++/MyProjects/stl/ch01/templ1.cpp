// templ1.cpp - show off some template features of C++20+
// Compile: g++/clang++ -std=c++23 .... -stdlib=libc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <print> // for std::println()
#include <string>
#include <typeinfo>
#include <vector>
#include "Points2D.h"

template <typename T>
T add_values(T a, T b, T c) {
  return a + b + c;
}

void templ1() {

  // add integers with add_values
  int a{10}, b{20}, c{30};
  int sum = add_values(a, b, c);
  std::println("a: {}, b: {}, c: {}, sum: {}", a, b, c, sum);

  // add doubles with add_values
  double d{100.0}, e{200.0}, f{300.0};
  double sum2 = add_values(d, e, f);
  std::println("d: {:.2f}, e: {:.2f}, f: {:.2f}, sum: {:.2f}", d, e, f, sum2);

  // will work for strings too!
  std::string s1{"Hello "}, s2{"C++ 23 "}, s3{"world!"};
  std::string sum3 = add_values(s1, s2, s3);
  std::println("s1: {:s}, s2: {:s}, s3: {:s}, sum: {:s}", s1, s2, s3, sum3);
}

// calculate mean for any numeric type
// NOTE: there is a "gotcha" in this function!
double calc_mean(auto a, auto b, auto c) { return (a + b + c) / 3.0; }

void templ2() {
  int a{12}, b{28}, c{36};

  double mean1 = calc_mean(a, b, c);
  std::println("a: {} b: {} c: {} -> mean: {:.3f}", a, b, c, mean1);

  float x{201.1f};
  long long y{108};
  unsigned short z{307};
  // I can pass different types as params are auto
  double mean2 = calc_mean(x, y, z);
  std::println("x: {} y: {} z: {} -> mean: {:.3f}", x, y, z, mean2);

  // compiler error here!!
  /*
  std::string s1{"Hello"}, s2{"C++"}, s3{"23"};
  double mean3 = calc_mean(s1, s2, s3);
  std::println("s1: {:s} s2: {:s} s3: {:s} -> mean: {:.3f}", s1, s2, s3, mean3);
  */
}

void templ3() {
  // use custom class
  Point2D<int> p1{10, 20};
  Point2D<int> p2{30, 40};
  Point2D<int> p3{50, 60};

  Point2D<int> p4 = add_values(p1, p2, p3);
  std::println("p1: {} p2: {} p3: {} -> add: {}", p1, p2, p3, p4);

  // co
}


int main(int /* argc*/, char **argv) {
  int rc{};

  try {
    std::println("\n---------- Results from templ1() ----------\n");
    templ1();
    templ2();
    templ3();
  }
  catch (const std::exception &ex) {
    rc = 1;
    std::println("Exception occured in {:s}", argv[0]);
    std::println("{:s}", ex.what());
  }
  return rc;
}
