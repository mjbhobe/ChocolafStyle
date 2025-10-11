// Points2D.h - declares Points2D class
#ifndef __Points2D_h__
#define __Points2D_h__

#include <concepts>
#include <ostream>

// constraint on data-type of Point2D class
template <typename T>
concept PointCoord2D = std::integral<T> || std::floating_point<T>;

template <PointCoord2D T>
class Point2D {
  // custom formatting class
  friend struct std::formatter<Point2D<T>>;

public:
  Point2D() = default;
  Point2D(T x, T y) : m_X{x}, m_Y{y} {};
  // accessors
  T X() const { return m_X; }
  T Y() const { return m_Y; }
  // for LHS (for example p2d.X()++
  T &X() { return m_X; }
  T &Y() { return m_Y; }

  // opertors
  friend bool operator==(const Point2D<T> &p1, const Point2D<T> &p2) {
    return (p1.m_X == p2.m_X) && (p1.m_Y == p2.m_Y);
  }
  friend bool operator!=(const Point2D<T> &p1, const Point2D<T> &p2) { return !(p1 == p2); }

  friend Point2D operator+(const Point2D &p1, const Point2D &p2) { return Point2D(p1.m_X + p2.m_X, p1.m_Y + p2.m_Y); }

  friend std::ostream &operator<<(std::ostream &ost, const Point2D &p) {
    ost << p.to_str();
    return ost;
  }

  // distance from origin
  double distance() const { return std::hypot(m_X, m_Y); }

private:
  T m_X{};
  T m_Y{};

  std::string to_str() const {
    std::string s;
    std::format_to(std::back_inserter(s), "({},{})", m_X, m_Y);
    return s;
  }
};

// formatter (so you can call this in std::format()
template <typename T>
struct std::formatter<Point2D<T>> : std::formatter<std::string> {
  constexpr auto parse(std::format_parse_context &fpc) { return fpc.begin(); }

  auto format(const Point2D<T> &point, std::format_context &ctx) const {
    return std::format_to(ctx.out(), "{}", point.to_str());
  }
};

#endif // __Points2D_h__
