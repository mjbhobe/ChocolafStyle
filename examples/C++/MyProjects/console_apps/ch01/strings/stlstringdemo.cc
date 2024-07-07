// stlstringdemo.cc - stringdemo.cc using STL strings
// compile: g++ ... -std=c++20 stlstringdemo.cc -o stlstringdemo -lstdc++
#include <cstdio>
#include <string>
#include <iostream>

int main(void) {
   std::string s1{"This "}, s2{"is a "}, s3{"concatenated string"};
   auto s4 = s1 + s2 + s3;
   std::cout << s4.c_str() << std::endl;
   std::cout << "Length of string: " << s4.length() << std::endl;
   std::cout << "Enter a sentence with whitespaced: ";
   ::fflush(stdin);
   std::string s5{""};
   std::getline(std::cin, s5);
   std::cout << "You entered: " << s5 << std::endl;
   return 0;
}
