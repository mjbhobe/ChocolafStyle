// -------------------------------------------------------
// Image.h - custom image class declaration
// -------------------------------------------------------
#ifndef __Image_h__
#define __Image_h__

#include <cstdint>
#include <format>
#include <ostream>
#include <string>
#include <vector>

class Image {
  using pixel_t = uint8_t;
  friend struct std::formatter<Image>;

public:
  Image() = default; // default compiler provided constructor
  Image(std::size_t height, std::size_t width);
  Image(const Image& im);
  Image(Image&& im) noexcept;
  virtual ~Image();

  Image& operator=(const Image& im);     // assignment opr
  Image& operator=(Image&& im) noexcept; // move opr

  // accessors
  std::size_t height() const { return m_Height; }
  std::size_t width() const { return m_Width; }
  std::size_t num_pixels() const { return m_Height * m_Width; }

  // relational operators
  friend bool operator==(const Image& m1, const Image& m2);
  friend bool operator!=(const Image& m1, const Image& m2);

  // output display
  friend std::ostream& operator<<(std::ostream& ost, const Image& im);

private:
  // member functions
  void reset();
  std::string to_string() const;

  // attributes
  std::size_t m_Height{};
  std::size_t m_Width{};
  std::vector<pixel_t> m_PixelBuff{};
};

// formatting helper
template <>
struct std::formatter<Image> : std::formatter<std::string>
{
  constexpr auto parse(std::format_parse_context& fpc) { return fpc.begin(); }

  auto format(const Image& im, std::format_context& fc) const
  {
    return std::format_to(fc.out(), "{}", im.to_string());
  }
};

#endif // __Image_h__
