#ifndef __MatPrint_h__
#define __MatPrint_h__

#include <iostream>
#include <sstream>      // For std::stringstream
#include <format>       // For std::formatter and std::format_context (which <print> implies)
#include <string_view>  // For using std::formatter<std::string_view>
#include <print>        // For std::println
#include <string>
#include <Eigen/Dense>


// Add this before main to enable C++23 formatting for Eigen matrices
template <typename Scalar, int Rows, int Cols, int Options, int MaxRows, int MaxCols>
struct std::formatter<Eigen::Matrix<Scalar, Rows, Cols, Options, MaxRows, MaxCols>> : std::formatter<std::string_view> {
    template <typename FormatContext>
    auto format(const Eigen::Matrix<Scalar, Rows, Cols, Options, MaxRows, MaxCols>& matrix, FormatContext& ctx) const {
        // Use Eigen's existing operator<< to convert the matrix to a string
        std::stringstream ss;
        ss << matrix;

        // Format the resulting string
        return std::formatter<std::string_view>::format(ss.str(), ctx);
    }
};

#endif  // __MatPrint_h__
