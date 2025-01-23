// templ.cpp - illustrates templates
// Compile: g++/clang++ -std=c++23 .... -lstdc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <cmath>
#include <concepts>
#include <iostream>
#include <ostream>
#include <print> // for std::println()
#include <stdexcept>
#include <string>
#include "Points2D.h"

template <typename T>
T add_values(T a, T b, T c)
{
  return a + b + c;
}

// calculate the mean of 3 numbers
// function decl without using templates (be careful not to pass in strings!!)
auto mean(auto a, auto b, auto c)
{
  return (a + b + c) / 3;
}

void templ_ex1()
{
  // adding integers
  int a{10}, b{20}, c{30};
  std::cout << std::format(
    "a: {} - b: {} - c: {} - a + b + c: {}\n", a, b, c, add_values(a, b, c));

  // adding doubles/floats
  double d{100.0}, e{225.45}, f{363.76};
  /*std::cout << */ std::println("d: {:.3f} - e: {:.3f} - f: {:.3f} - d + e + f: {:.3f}",
    d, e, f, add_values(d, e, f));

  // adding strings
  std::string h{"Hello "}, i{"C++ "}, j{"23. You rock!"};
  std::cout << std::format("h: \"{}\" - i: \"{}\" - j: \"{}\" - h + i + j: \"{}\"\n", h,
    i, j, add_values(h, i, j));

  // calculating means (of ints)
  std::cout << std::format(
    "a: {} - b: {} - c: {} - mean(a, b, c): {}\n", a, b, c, mean(a, b, c));

  // calculating means (of doubles)
  std::cout << std::format("d: {:.3f} - e: {:.3f} - f: {:.3f} - mean(d, e, f): {:.3f}\n",
    d, e, f, mean(d, e, f));
}

void templ_ex2()
{
  // call functions of Point2D<T> class

  Point2D<int> p1{10, 20}, p2{30, 40}, p3{50, 60};
  // add & display
  std::println(
    "p1: {} - p2: {} - p3: {} - p1+p2+p3: {}", p1, p2, p3, add_values(p1, p2, p3));

  // test equality operators
  std::println("p1 == p2? {}", p1 == p2);
  std::println("p1 == p1? {}", p1 == p1);
  std::println("p1 != p1? {}", p1 != p1);
  std::println("p1 != p2? {}", p1 != p2);

  // scale p1 (accessing members p1.X(), p1.Y()
  Point2D<int> p4{p1.X() * 10, p1.Y() * 20};
  std::println("p1: {} - p4: {} [=p1.X()*10, p1.Y()*20]", p1, p4);
  // p1.X(), p1.Y() LHS
  p1.X() /= 5;
  p1.Y() /= 4;
  std::println("p1: {} [p1.X()/=5, p1.Y()/=4]", p1);
  // measuring distance
  std::println("p2: {} - p2.distance(): {} [{}]", p2, p2.distance(),
    sqrt(std::pow(p2.X(), 2) + std::pow(p2.Y(), 2)));

  // Point2D<double>
  Point2D<double> p5{100.0, 200.0};
  Point2D<double> p6{300.0, 400.0};
  Point2D<double> p7{500.0, 600.0};
  Point2D<double> p8 = add_values(p5, p6, p7);
  std::println("p5: {} p6: {} p7: {} p8: {}", p5, p6, p7, p8);

  // test equality operators
  std::println("p5 == p6? {}", p5 == p6);
  std::println("p5 == p5? {}", p5 == p5);
  std::println("p5 != p5? {}", p5 != p5);
  std::println("p5 != p6? {}", p5 != p6);

  // scale p5 (accessing members p5.X(), p5.Y()
  Point2D<double> p9{p5.X() * 10, p5.Y() * 20};
  std::println("p5: {} - p9: {} [=p5.X()*10, p5.Y()*20]", p5, p9);
}

int main(void)
{
  templ_ex1();
  templ_ex2();
  return EXIT_SUCCESS;
}
