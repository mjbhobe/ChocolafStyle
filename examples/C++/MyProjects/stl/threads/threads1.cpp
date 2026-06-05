#include <iostream>
#include <thread>

constexpr int NUM_TIMES = 500;

void func1()
{
  for (int i = 0; i < NUM_TIMES; i++)
    std::cout << "+";
}

void func2()
{
  for (int i = 0; i < NUM_TIMES; i++)
    std::cout << "-";
}


int main(void)
{
  std::thread worker1(func1);
  std::thread worker2(func2);

  // start the threads
  worker1.join();
  worker2.join();

  return 0;
}
