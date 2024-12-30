// strings.cpp - testing string functions
// Compile: g++/clang++ -std=c++23 .... -lstdc++

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <string>
#include <print>    // for std::println()

int main(void) {
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
  std::println("s1 == s2 : {}", s1==s2);
  std::println("s1 == s1 : {}", s1==s1);
  std::println("s1 != s2 : {}", s1!=s2);
  std::println("s1 < s2 : {}", s1<s2);
  std::println("s1 <= s2 : {}", s1<=s2);
  std::println("s1 <= s1 : {}", s1<=s1);
  std::println("s1 > s2 : {}", s1>s2);
  std::println("s1 >= s2 : {}", s1>=s2);
  std::println("s2 >= s2 : {}", s2>=s2);

  // find
  std::println("s3: {} - s2: {}", s3, s2);
  std::size_t pos = s3.find(s2);
  if (pos != std::string::npos)
    std::println("Found \"{}\" in {} at pos {}", s2, s3, pos);
  else
    std::println("\"{}\" NOT found in {}", s2, s3);

  // find & replace
  std::string s4{"Anupa!"};
  std::size_t pos2 = s3.find(s2);  // try to find
  if (pos2 != std::string::npos) {
    // found - replace with s4
    // I need s3 as before after this call, so making copy
    std::string s5{s3}; 
    s5.replace(pos2 /* from this pos */, s2.size() /* these many chars */,
        s4 /* with this */);
    std::println("After replace: {}", s5);
  }
  else
    std::println("\"{}\" NOT found in {}", s2, s3);




  return EXIT_SUCCESS;
}
