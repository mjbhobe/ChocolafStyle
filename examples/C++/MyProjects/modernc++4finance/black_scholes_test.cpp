#include <print>
#include "black_scholes.h"

int main(void)
{
  double strike         = 75.0;
  auto payoff_type      = PayoffType::Call;
  double spot           = 100.00;
  double rate           = 0.05;
  double time_to_expire = 0.0; // now!
  double volatility     = 0.25;

  // calculate value of ITM Call
  BlackScholes bsc_itm_call(
      strike, spot, time_to_expire, PayoffType::Call, rate);
  double value = bsc_itm_call(volatility);
  std::println("Value of ITM call: {:.3f}", value);

  return EXIT_SUCCESS;
}
