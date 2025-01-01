// strings.cpp - testing string functions
// Compile: g++/clang++ -std=c++23 .... -lstdc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <print> // for std::println()
#include <string>

int main(void)
{
  // display & compare various types of strings
  const std::string s1{"Yo"};
  const std::string s2{"Manish"};
  const char c{'!'};
  const char* s = "How are you?";

  // print each type
  std::println("s1: {} - s2: {} - c: {} - s: {}", s1, s2, c, s);

  // string concatenation
  // you can concatenate string to string | char | const char*
  std::string s3 = s1 + ' ' + s2 + ' ' + s;
  std::println("s3: {}", s3);

  // comparison (usual operators available ==, !=, <, >, <=, >=
  std::println("s1 == s2 : {}", s1 == s2);
  std::println("s1 == s1 : {}", s1 == s1);
  std::println("s1 != s2 : {}", s1 != s2);
  std::println("s1 < s2 : {}", s1 < s2);
  std::println("s1 <= s2 : {}", s1 <= s2);
  std::println("s1 <= s1 : {}", s1 <= s1);
  std::println("s1 > s2 : {}", s1 > s2);
  std::println("s1 >= s2 : {}", s1 >= s2);
  std::println("s2 >= s2 : {}", s2 >= s2);

  // find
  std::println("s3: {} - s2: {}", s3, s2);
  std::size_t pos = s3.find(s2);
  if (pos != std::string::npos)
    std::println("Found \"{}\" in {} at pos {}", s2, s3, pos);
  else
    std::println("\"{}\" NOT found in {}", s2, s3);

  // find & replace
  std::string s4{"Anupa!"};
  std::size_t pos2 = s3.find(s2); // try to find
  if (pos2 != std::string::npos) {
    // found - replace with s4
    // I need s3 as before after this call, so making copy
    std::string s5{s3};
    s5.replace(pos2 /* from this pos */, s2.size() /* these many chars */,
      s4 /* with this */);
    std::println("After replace: {}", s5);
  }
  else {
    std::println("\"{}\" NOT found in {}", s2, s3);
  }

  // starts_with & ends_with
  const std::string s6{"apple banana orange strawberry pear"};
  const std::string_view sv1{"apple"};
  const std::string_view sv2{"pear"};
  const std::string_view sv3{"strawberry"};

  bool b1 = s6.starts_with(sv1);
  bool b2 = s6.ends_with(sv2);
  std::println("\'{}\' starts with string \'{}\' - {}", s6, sv1, b1);
  std::println("\'{}\' ends with string \'{}\' - {}", s6, sv2, b2);

#ifdef __cpp_lib_string_contains
  bool b3 = s6.contains(sv3);
  std::println("\'{}\' contains \'{}\' - {}", s6, sv3, b3);
#endif

  return EXIT_SUCCESS;
}
