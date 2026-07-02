// ============================================================================
// black_sholes.cpp : implements the Black Scholes options pricing algorithm.
//
// My experiments with C/C++, STL & Qt Framework
// Code is shared for learning purposes only!
// ============================================================================
#include <cmath>
#include <numbers>
#include "black_scholes.h"

BlackScholes::BlackScholes(double strike_price, double spot,
    double time_to_expire, PayoffType payoff_type, double rate, double dividend)
    : m_strike{strike_price}, m_spot{spot}, m_time_to_expire{time_to_expire},
      m_payoff_type{payoff_type}, m_rate{rate}, m_dividend{dividend}
{
}


double BlackScholes::operator()(double volatility)
{
  using std::exp;

  const int phi = static_cast<int>(m_payoff_type);

  if (m_time_to_expire > 0.0) {
    auto norm_args = _compute_norm_args(volatility);
    double d1      = norm_args[0];
    double d2      = norm_args[1];

    auto norm_cdf = [](double x) {
      return (1.0 + std::erf(x / std::numbers::sqrt2)) / 2.0;
    };

    double nd_1      = norm_cdf(phi * d1);
    double nd_2      = norm_cdf(phi * d2);
    double disc_fctr = exp(-m_rate * m_time_to_expire);

    return phi *
        (m_spot * exp(-m_dividend * m_time_to_expire) * nd_1 -
            disc_fctr * m_strike * nd_2);
  }
  else {
    return std::max(phi * (m_spot - m_strike), 0.0);
  }
}
