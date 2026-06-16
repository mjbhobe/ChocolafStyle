// Hello.cpp - cannonical Hello World!
// compile: clang++ -std=c++23 Hello.cpp -o Hello -stdlib=libc++
#include <print>

int main(void)
{
  // NOTE: std::println() will work with C++ 23 compiler ONLY!
  std::println("Hello World!\n");
  return EXIT_SUCCESS;
}
