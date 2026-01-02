// ----------------------------------------------------------------------
// stl_utils.h - utility functions to use with the STL
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

// generate a random integer between lower & upper (both inclusive!)
inline size_t random_int_between(size_t lower = 0, size_t upper = 100)
{
  static std::random_device rd;                            // seed
  static std::mt19937 gen(rd());                           // Mersenne Twister engine
  std::uniform_int_distribution<size_t> distrib(lower, upper); // range(min,max) - both inclusive
  return distrib(gen);
}

template<typename T>
T random_pick_from_vector(const std::vector<T> &vec)
{
  size_t rand_index = random_int_between(0, vec.size() - 1);
  return vec[rand_index];
}

template<typename T>
std::vector<T> random_vec(size_t num_elems, size_t lower = 0, size_t upper = 100)
{
  // generate vector of num_elem random integers between min & max
  std::vector<T> vec;
  vec.reserve(num_elems);
  std::generate_n(
    std::back_inserter(vec), num_elems,
    [&]() mutable { return random_int_between(lower, upper); }
  );
  // for (size_t i = 0; i < num_elems; i++)
  //   vec.push_back(static_cast<T>(random_int_between(min, max)));
  return vec;
}


// ------------------------------------------------------------------------------------
// custom formatter for std::vector<T> so you can use it like above with C++23's
// std::print() and std::println() functions.
// Works with both std::string & std::wstring
// ------------------------------------------------------------------------------------

template<typename T, typename CharT>
struct std::formatter<std::vector<T>, CharT> : std::formatter<CharT> {
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
