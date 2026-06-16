#include <type_traits>

int main(void)
{
  static_assert(std::is_object_v<int>);
  static_assert(std::is_object_v<decltype(main)>);
}
