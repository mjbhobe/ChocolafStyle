#ifndef FINCALCULATIONS_H
#define FINCALCULATIONS_H

// #include <bits/stdc++.h>
#include <algorithm>
#include <concepts>
#include <vector>

namespace fincalc {

/**
 * @brief The Equities class
 * Financial calculations for Equity price series
 * Algos from the book "Practical C++ 20 for Financial Programming by Carlos
 * Oliveira (APress)
 */

template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <typename T>
  requires Numeric<T>
class Equities {
public:
  static std::vector<T> ma(const std::vector<T> &prices, size_t num_periods) {
    /**
     * @brief ma
     * Calculates the moving average (MA) of prices for a given num periods
     * @param prices (std::vector<float>) - the prices series
     * @param num_periods (size_t) - number of periods for MA calculation
     * @returns ma series (std::vector<float>)
     */
    std::vector<T> ma{};
    double sum{0.0};

    // cycle over the prices
    for (size_t i = 0; i < prices.size(); ++i) {
      sum += prices[i];
      if (i >= num_periods) {
        ma.push_back(sum / num_periods);
        sum -= prices[i - num_periods];
      }
    }
    return ma;
  }

  static std::vector<T> ema(const std::vector<T> &prices, size_t num_periods) {
    /**
     * @brief ema
     * Calculates the exponential moving average (EMA) of prices for a given
     *      number of periods
     * @param prices (std::vector<float>) - the prices series
     * @param num_periods (size_t) - number of periods for MA calculation
     * @returns ema series (std::vector<float>)
     */
    std::vector<T> ema{};
    double multiplier{2.0 / (num_periods + 1)};

    // calculate MA to determine first element corresponding to
    // given number of periods
    std::vector<T> ma = Equities<T>::ma(prices, num_periods);
    ema.push_back(ma.front());

    // for remaining elements, compute weighted avarage
    for (size_t i = num_periods + 1; i < prices.size(); ++i) {
      T val = static_cast<T>((1 - multiplier) * ema.back() +
                             multiplier * prices[i]);
      ema.push_back(val);
    }
    return ema;
  }

  static T range(const std::vector<T> &prices) {
    /**
     * @brief range
     * Calculates the range (max - min) across a price series
     * @param prices (std::vector<float>) - the price series
     * @return range (= max(prices) - min(prices)) across series
     */
    //    T min_val = *min_element(prices.begin(), prices.end());
    //    T max_val = *max_element(prices.begin(), prices.end());
    //    return max_val - min_val;
    auto min_max_pair = std::minmax_element(prices.begin(), prices.end());
    return *(min_max_pair.second) - *(min_max_pair.first);
  }

  static T avgDailyRange(const std::vector<T> &prices) {
    /**
     * @brief avgDailyRange
     * Calculates the average daily range of prices across price time series
     * For each day, calculate daily_range = (price_today - price_yesterday)
     * The calculate average of daily_range across series
     * @param prices (std::vector<float>) - the price series
     * @return range (= double) - average daily range across price series
     */
    if (prices.size() < 2)
      return static_cast<T>(0.0);

    T sum{0.0};
    T prev = prices[0];

    for (size_t i = 1; i < prices.size(); ++i) {
      T range = std::abs(prices[i] - prev);
      sum += range;
    }
    return sum / (prices.size() - 1);
  }

  // calculate average prices (or mean)
  static double mean(const std::vector<T> &prices) {
    return (std::accumulate(prices.cbegin(), prices.cend(), 0.0)) /
           prices.size();
  }

  // calculate std-deviation of prices
  static double stdDev(const std::vector<T> &prices) {
    T mu = mean(prices);

    // Calculate the variance of the data
    double variance{0.0};
    for (size_t i = 0; i < prices.size(); i++) {
      variance += (prices[i] - mu) * (prices[i] - mu);
    }

    // Calculate the standard deviation of the data
    return sqrt(variance / prices.size());
  }

  // correlation between two instrument price series
  static double corr(const std::vector<T> &prices1,
                     const std::vector<T> &prices2) {

    if (prices1.size() != prices2.size())
      throw "Prices series should have same size!";

    double mean1 = mean(prices1);
    double mean2 = mean(prices2);
    double stdDev1 = stdDev(prices1);
    double stdDev2 = stdDev(prices2);

    double sum{0.0};
    // calculate sum([x_i - x_bar] * [y_i - y_bar])
    for (size_t i = 0; i < prices1.size(); ++i)
      sum += (prices1[i] - mean1) * (prices2[i] - mean2);
    // sum([x_i - x_bar] * [y_i - y_bar])/(s_x * s_y)
    sum /= (stdDev1 * stdDev2);
    // calculate average of above
    return sum / (prices1.size() - 1);
  }

}; // class FinCalculator

} // namespace fincalc

#endif // FINCALCULATIONS_H
