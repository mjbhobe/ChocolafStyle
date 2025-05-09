#include <print>
#include <sstream>
#include <string>
#include <vector>

template <typename T>
std::string vec2str(const std::vector<T>& vec)
{
  std::ostringstream oss;
  oss << "[";
  for (size_t i = 0; i < vec.size(); ++i) {
    oss << vec[i];
    if (i < vec.size() - 1)
      oss << ", ";
  }
  oss << "]";
  return oss.str();
}

int main(void)
{
  std::vector<int> vec1{2, 4, 6, 8, 10};

  std::println("Vector: {}", vec2str(vec1));

  return EXIT_SUCCESS;
}
