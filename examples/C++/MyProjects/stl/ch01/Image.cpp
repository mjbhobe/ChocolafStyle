// --------------------------------------------------------
// Image.cpp - Image class implementation
// --------------------------------------------------------

// require C++ 23
#if __cplusplus < 202302L
#error This code required a C++23 standards compliant C++ compiler!
#error Please enable C++23 support (e.g. For g++/clang++ use -std=c++23)
#endif

#include <cstdint>
#include <format>
#include <ostream>
#include <print>
#include <string>
#include <utility>
#include <vector>
#include "Image.h"

Image::Image(std::size_t height, std::size_t width) : m_Height(height), m_Width(width)
{
  m_PixelBuff.resize(m_Height * m_Width);
}

Image::Image(const Image& im) :
  m_Height(im.m_Height), m_Width(im.m_Width), m_PixelBuff(im.m_PixelBuff)
{}

// move constructor
Image::Image(Image&& im) noexcept :
  m_Height(im.m_Height), m_Width(im.m_Width), m_PixelBuff{std::move(im.m_PixelBuff)}
{
  im.reset();
}

Image::~Image()
{
  std::println("Image::~Image() {}", this->to_string());
}

// copy assignment
Image& Image::operator=(const Image& im)
{
  m_Height = im.m_Height;
  m_Width = im.m_Width;
  m_PixelBuff = im.m_PixelBuff;
  return *this;
}

// move assignment
Image& Image::operator=(Image&& im) noexcept
{
  m_Height = im.m_Height;
  m_Width = im.m_Width;
  m_PixelBuff = std::move(im.m_PixelBuff);
  im.reset();
  return *this;
}

bool operator==(const Image& im1, const Image& im2)
{
  if (im1.m_Height != im2.m_Height || im1.m_Width != im2.m_Width)
    return false;

  return im1.m_PixelBuff == im2.m_PixelBuff;
}

bool operator!=(const Image& im1, const Image& im2)
{
  return !operator==(im1, im2);
}

std::ostream& operator<<(std::ostream& ost, const Image& im)
{
  ost << im.to_string();
  return ost;
}

void Image::reset()
{
  m_Height = 0;
  m_Width = 0;
}

std::string Image::to_string() const
{
  std::string s{};
  std::format_to(std::back_inserter(s), "[{:5d} ", m_Height);
  std::format_to(std::back_inserter(s), "[{:5d} ", m_Width);
  std::format_to(std::back_inserter(s), "[{:8d} ", m_Height * m_Width);

  constexpr int pb_w{(sizeof(void*) <= 4) ? 8 : 16};
  std::uintptr_t pb = reinterpret_cast<std::uintptr_t>(m_PixelBuff.data());
  std::format_to(std::back_inserter(s), "0x{:0>{}X}]", pb, pb_w);
  return s;
}

// -----------------------------------------------
// main()
// -----------------------------------------------

int main(void)
{
  Image im0{};
  std::println("im0: {} - after ctor", im0);
  Image im1{100, 200};
  std::println("im1: {} - after ctor", im1);
  Image im2{300, 400};
  std::println("im2: {} - after ctor", im2);

  return EXIT_SUCCESS;
}
