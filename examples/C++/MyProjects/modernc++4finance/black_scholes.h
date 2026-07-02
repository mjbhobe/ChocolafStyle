// ============================================================================
// black_sholes.h : declares a class that implements the Black Scholes
//     options pricing algorithm.
//
// My experiments with C/C++, STL & Qt Framework
// Code is shared for learning purposes only!
// ============================================================================
#ifndef __black_scholes_h__
#define __black_scholes_h__

#include <array>

enum class PayoffType {
  Call = 1,
  Put  = -1,
};

class BlackScholes {
  public:
    BlackScholes(double strike_price, double spot, double time_to_expire,
        PayoffType payoff_type, double rate, double divident = 0.0);
    double operator()(double volatility);
  private:
    std::array<double, 2> _compute_norm_args(double volatility);

    double m_strike, m_spot, m_time_to_expire;
    PayoffType m_payoff_type;
    double m_rate, m_dividend;
};

#endif // __black_scholes_h__
