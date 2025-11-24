// ----------------------------------------------------------------------
// stl_utils.cpp - utility functions to use with the STL
//
// @Author: Manish Bhobe
// Code shared for learning purposes only! Use at your own risk
// ----------------------------------------------------------------------

#ifndef __Stl_Utils_h__
#define __Stl_Utils_h__

// require C++23 compiler!!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <format>
#include <iostream>
#include <print>
#include <random>
#include <vector>

// function to enable you to do std::cout << vector_instance
template<typename T>
std::ostream &operator<<(std::ostream &ost, const std::vector<T> &vec)
{
  auto vec_size = vec.size();

  ost << "[";
  for (int i = 0; i < vec_size - 1; i++)
    ost << vec[i] << ", ";
  ost << vec[vec_size - 1] << "]";
  return ost;
}

// random select an integer between min & max (both inclusive!)
size_t random_int(size_t min, size_t max)
{
  static std::random_device rd;                            // seed
  static std::mt19937 gen(rd());                           // Mersenne Twister engine
  std::uniform_int_distribution<size_t> distrib(min, max); // range(min,max) - both inclusive
  return distrib(gen);
}

template<typename T>
T random_pick_from_vector(const std::vector<T> &vec)
{
  size_t rand_index = random_int(0, vec.size() - 1);
  return vec[rand_index];
}

// ------------------------------------------------------------------------------------
// custom formatter for std::vector<T> so you can use it like above with C++23's
// std::print() and std::println() functions. Should work with both std::string &
// std::wstring
// ------------------------------------------------------------------------------------

template<typename T, typename CharT>
struct std::formatter<std::vector<T>, CharT> {
    constexpr auto parse(std::basic_format_parse_context<CharT> &ctx) { return ctx.begin(); }

    template<typename FormatContext>
    auto format(const std::vector<T> &vec, FormatContext &ctx) const
    {
      auto out = std::format_to(ctx.out(), "[");

      for (size_t i = 0; i < vec.size(); ++i) {
        out = std::format_to(out, "{}", vec[i]);
        if (i < vec.size() - 1) {
          out = std::format_to(out, ", ");
        }
      }

      return std::format_to(out, "]");
    }
};


#endif // __Stl_Utils_h__
