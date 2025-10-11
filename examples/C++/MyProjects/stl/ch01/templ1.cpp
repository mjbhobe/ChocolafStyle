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

template <typename T>
T add_values(T a, T b, T c) {
  return a + b + c;
}

void templ1() {
  // uniform initialization
  int a{10}, b{20}, c{30};

  // add integers with add_values
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

int main(int /* argc*/, char **argv) {
  int rc{};

  try {
    std::println("\n---------- Results from templ1() ----------\n");
    templ1();
  }
  catch (const std::exception &ex) {
    rc = 1;
    std::println("Exception occured in {:s}", argv[0]);
    std::println("{:s}", ex.what());
  }
  return rc;
}
