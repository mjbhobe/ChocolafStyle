#include <concepts>
#include <cstdlib>
#include <format>
#include <iomanip>
#include <iostream>
#include <locale>
#include <random>
#include <sstream>
#include <vector>

// some locales to use
auto us_locale = std::locale("en_US.UTF-8"); // US
auto de_locale = std::locale("de_DE.UTF-8"); // German
auto in_locale = std::locale("hi_IN.UTF-8"); // Indian

/* locale specific number formatting */
// Concept to check if T is an integer or floating-point type
template <typename T>
concept Numeric = std::is_integral_v<T> || std::is_floating_point_v<T>;

// Custom formatter for locale-aware number formatting
template <typename CharT> struct locale_formatter_number {
  std::locale locale;

  template<Numeric T>
  constexpr auto operator()(const T &value) const
  {
    return std::format_to(std::ostreambuf_iterator<CharT>(), locale, "{:.4f}", value);
  }
};

// Custom formatter for locale-aware currency formatting
template <typename CharT> struct locale_formatter_currency {
  std::locale locale;

  template <Numeric T> constexpr auto operator()(const T &value) const {
    // NOTE: only difference between number & currency is format spec (.4f vs
    // .4c)
    return std::format_to(std::ostreambuf_iterator<CharT>(), locale, "{:.4c}", value);
  }
};

/**
 * displays all elements in a vector separated by space
 */
template <typename T>
std::ostream &operator<<(std::ostream &ost, const std::vector<T> &v) {
  /* NOTE: T should have << operator that allows it to be displayed
   * on ostream. All standard data types ok. Needed for custom classes
   */
  for (const T e : v)
    ost << e << ' ';
  ost << std::endl;
  return ost;
}

// Function to format a floating-point value as number using a specific locale
std::string format_as_number(float val, std::locale &loc)
{
  // Create a stringstream and imbue it with the locale
  std::stringstream ss;
  ss.imbue(loc);

  // Use std::put_money to format the val as currency
  ss << std::showbase << std::fixed << val;
  //   << std::put_money(val * 100); // Multiply by 100 for put_money

  return ss.str();
}

// Function to format a floating-point value as currency using a specific locale
std::string format_as_currency(float val, std::locale &loc) {
  // Create a stringstream and imbue it with the locale
  std::stringstream ss;
  ss.imbue(loc);

  // Use std::put_money to format the val as currency
  ss << std::showbase
     << std::put_money(val * 100); // Multiply by 100 for put_money

  return ss.str();
}

// user defined type
class Employee {
public:
  Employee(size_t empNo, const std::string &name, float salary)
      : m_empNo(empNo), m_name(name), m_salary(salary) {}
  // getters & setters
  size_t empNo() const { return m_empNo; }
  std::string name() const { return m_name; }
  void setName(const std::string &newName) {
    if (m_name != newName)
      m_name = newName;
  }
  float salary() const { return m_salary; }
  void setSalary(float newSal) {
    if (newSal >= float(0.0)) {
      m_salary = newSal;
    } else {
      throw std::invalid_argument(
          std::format("Salary ({:.3f}) parameter cannot be -ve", newSal));
    }
  }

  std::string toString() const {
    return std::format("Employee -> No: {:<3d} - name: {:s} - salary: {:s}",
                       m_empNo, m_name,
                       format_as_currency(m_salary, in_locale));
  }

  friend std::ostream &operator<<(std::ostream &ost, const Employee &emp) {
    ost << emp.toString() << std::endl;
    return ost;
  }

private:
  size_t m_empNo;
  std::string m_name;
  float m_salary;
};

namespace mjb {

  double randn(double start, double end)
  {
    // generate 1 random number from standard normal distribution
    // and rescale it between start & end

    // create the normal distribution & generator
    std::random_device rd{};
    std::mt19937 gen{rd()};

    // create normal distribution with mean = 0 & std = 1.0
    // (i.e. a standard normal distribution)
    std::normal_distribution<double> distribution{0, 1};
    double randomNumber = distribution(gen);
    // rescale it to between start & end
    // randomNumber = start + (randomNumber + 3) * (end - start) / 6;
    randomNumber = start + (randomNumber + 1) * (end - start) / 2;
    return randomNumber;
  }

  std::vector<double> randn(size_t num, double start, double end)
  {
    // generates num random numbers between start & end
    // from standard normal distribution

    // Generate N random numbers and store them in a vector
    std::vector<double> nums(num);
    // populate with random numbers
    std::generate(nums.begin(), nums.end(), [&]() { return randn(start, end); });
    return nums;
  }
} // namespace mjb

int main(void) {
  // initialize random number generator
  constexpr unsigned int SEED{42};

  // has auto-deduced vector as stl::vector<int>
  std::vector vec{1, 2, 3, 4, 5};

  // display all elements
  /*
  for (const auto elem : vec) {
    std::cout << elem << " ";
  }
  std::cout << std::endl;
  */
  std::cout << vec;

  // resise & print
  vec.resize(vec.size() + 2);
  // display all elements
  std::cout << vec;

  // custom classes in vectors
  std::vector<Employee> emps{
      Employee(10, "Manish", 45678.67),
      Employee(20, "Anupa", 86789.75),
      Employee(30, "Nupoor", 6789.83),
  };
  for (auto const &e : emps)
    std::cout << e.toString() << std::endl;

  //  givs Nups a hike of 20%
  auto nups = emps[2];
  nups.setSalary(1.2 * nups.salary());
  std::cout << "Post salary hike: " << nups.toString() << std::endl;

  // select random employee
  std::mt19937 gen(SEED); // Mersenne Twister engine seeded SEED
  std::uniform_int_distribution<> dis(0, emps.size());
  auto index = dis(gen);
  std::cout << "emps[" << index << "] = " << emps[index].toString()
            << std::endl;
  std::cout << "123456789.45678 as currecy is "
            << format_as_currency(123456789.45678, in_locale) << std::endl;
  std::cout << "123456789.45678 as number is "
            << format_as_number(123456789.45678, in_locale) << std::endl;

  // vector of vectors
  std::vector<std::vector<double>> X(4);
  // the first one is a random set of 20 numbers between 50 & 200
  X[0] = mjb::randn(10, -200, 200);
  std::cout << "randn(): " << X[0] << std::endl;
  // for each element of X[0] add a random number between -3o & +30
  X[1] = std::vector<double>(X[0].size());
  std::transform(X[0].cbegin(), X[0].cend(), X[1].begin(), [](double x) {
    return x + mjb::randn(-30, +30);
  });
  std::cout << "X[1]: " << X[1] << std::endl;
  X[2] = std::vector<double>(X[0].size());
  std::transform(X[0].cbegin(), X[0].cend(), X[2].begin(), [](double x) {
    return x > 50 ? +1. : -1.;
  });
  std::cout << "X[2]: " << X[2] << std::endl;
  X[3] = std::vector<double>(X[0].size());
  std::transform(X[0].cbegin(), X[0].cend(), X[3].begin(), [](double x) {
    return x + std::cos(mjb::randn(-30, +30));
  });
  std::cout << "X[3]: " << X[3] << std::endl;

  return EXIT_SUCCESS;
}
