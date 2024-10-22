// MemoryBlock.cc - testing MemoryBlock class
#include <iostream>
#include <vector>
#include "MemoryBlock.h"

int main(void)
{
  std::vector<MemoryBlock> v;

  v.push_back(MemoryBlock(25));
  MemoryBlock blk = MemoryBlock(75);
  v.push_back(blk);
  return 0;
}


