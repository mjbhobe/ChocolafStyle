// MemoryBlock.h - class declaration
#ifndef __MemoryBlock_h__
#define __MemoryBlock_h__

#include <iostream>
#include <algorithm>

template<typename T>
class MemoryBlock {
  protected:
    size_t _length;
    T *_data;
  public:
    explicit MemoryBlock(size_t length)
      : _length(length), _data(new int[length])
    {
      std::cout << "In MemoryBlock(size_t). length = "
        << _length << std::endl;
    }

    ~MemoryBlock()
    {
      std::cout << "In ~MemoryBlock(). length = "
        << _length << ".";
      if (_data != nullptr) {
        std::cout << " Deleting resources.";
        delete [] _data;
      }
      std::cout << std::endl;
    }

    // copy constructor
    MemoryBlock(const MemoryBlock& other)
      : _length(other._length), _data(new int[other._length])
    {
      std::cout << "In MemoryBlock(const MemoryBlock&). length = "
        << _length << std::endl;
      // copy data
      std::copy(other._data, other._data + _length, _data);
    }

    // copy assignment
    MemoryBlock& operator = (const MemoryBlock& other)
    {
      std::cout << "In operator = (const MemoryBlock&). length = "
        << other._length << ". Copying resources." << std::endl;
      if (this != &other) {
        _length = other._length;
        _data = new int[_length];
        std::copy(other._data, other._data + _length, _data);
      }
      return *this;
    }

    size_t length() const 
    {
      return _length;
    }
};


#endif   // __MemoryBlock_h__
