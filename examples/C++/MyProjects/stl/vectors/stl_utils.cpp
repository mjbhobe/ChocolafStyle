// ----------------------------------------------------------------------
// stl_utils.cpp - utility functions to use with the STL
//
// @Author: Manish Bhobe
// Code shared for learning purposes only! Use at your own risk
// ----------------------------------------------------------------------

// require C++23 compiler!!
#if __cplusplus < 202302L && (!defined(_MSVC_LANG) || _MSVC_LANG < 202004L)
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <format>
#include <iostream>
#include <print>
#include <random>
#include <vector>

#include "stl_utils.h"

// random select an integer between min & max (both inclusive!)
size_t random_int_between2(size_t lower /*=0*/, size_t upper /*=100*/)
{
  static std::random_device rd;                                // seed
  static std::mt19937 gen(rd());                               // Mersenne Twister engine
  std::uniform_int_distribution<size_t> distrib(lower, upper); // range(min,max) - both inclusive
  return distrib(gen);
}
