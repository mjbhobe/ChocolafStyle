// fin02.cpp: calculate annutities
// Compile: g++/clang++ -std=c++23 .... -stdlib=libc++  // on Windows with clang++
// Compile: g++/clang++ -std=c++23 .... -lstdc++        // on Mac or Linux

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <print> // NOTE: supported on C++ 23 standard only


int main(void)
{
  std::println("Hello! Welcome to Financial programming with C++");
  return EXIT_SUCCESS;
}
