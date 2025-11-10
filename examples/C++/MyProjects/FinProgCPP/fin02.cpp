// fin02.cpp: calculate annutities
// Compile: g++/clang++ -std=c++23 .... -stdlib=libc++  // on Windows with clang++
// Compile: g++/clang++ -std=c++23 .... -lstdc++        // on Mac or Linux

// require C++ 23!
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler.
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <cstdio>
#include <iostream>
#include <locale>
#include <print> // NOTE: supported on C++ 23 standard only


const int MONTHS_IN_YEAR = 12;

int main(void)
{
  // set initial values
  double principal = 100'000.0;
  double interestRate = 0.05; // 5%
  int yearsOfLoan = 30;

  // let's use Indian locale for printing numbers
  std::locale indian_locale("en_IN.UTF-8");
  std::cout.imbue(indian_locale);

  ::fflush(stdin);

  // read from user
  std::print("Enter principal: ");
  std::cin >> principal;
  std::print("Enter interest rate: ");
  std::cin >> interestRate;
  std::print("Enter years of loan: ");
  std::cin >> yearsOfLoan;

  double monthInterest = interestRate / MONTHS_IN_YEAR;
  long monthsInYear = yearsOfLoan * MONTHS_IN_YEAR;

  // print values, respective locale set above
  std::println("Principle: {:.3fL} - Interest: {:.6fL} - Years of Loan: {:L}", principal, interestRate, yearsOfLoan);
  std::println("Monthly Interest: {:.6L}", monthInterest);


  return EXIT_SUCCESS;
}
