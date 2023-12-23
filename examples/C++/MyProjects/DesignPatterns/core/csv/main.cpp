#include <fmt/core.h>
#include <fmt/ranges.h>

#include <iostream>
#include <map>
#include <numeric>
#include <string>
#include <vector>

#include "FinCalculations.h"
#include "rapidcsv.h"

typedef std::map<std::string, std::vector<float>> PricesMap;

template<typename T>
void display_vector(const std::vector<T> &vec, const std::string_view prompt = "")
{
   if (prompt.length() > 0)
      std::cout << prompt << std::endl;
   for (auto iter = vec.cbegin(); iter != vec.cend(); ++iter)
      std::cout << *iter << ", ";
   std::cout << std::endl;
}

bool cmp(std::pair<std::string, float> &one, std::pair<std::string, float> &two)
{
   if (one.second == two.second)
      // if corr is same, sort asc by symbol
      return one.first < two.first;
   return one.second > two.second;
}

std::vector<std::pair<std::string, float>> sort_on_corr_desc(
      std::map<std::string, float> &corr_map
)
{
   std::vector<std::pair<std::string, float>> A;
   for (auto &it : corr_map)
      A.push_back(std::make_pair(it.first, it.second));
   std::sort(A.begin(), A.end(), cmp);
   return A;
}

PricesMap loadPrices(const std::string field = "Adj Close")
{
   // load prices
   PricesMap prices;

   // holdings.csv holds my portfolio
   rapidcsv::Document holdings("holdings.csv");
   std::vector<std::string> symbols = holdings.GetColumn<std::string>("PFOLIO");
   for (auto iter = symbols.begin(); iter != symbols.end(); ++iter) {
      // load the stock prices file
      std::string prices_file = fmt::format("{}.csv", *iter);
      rapidcsv::Document prices_data(prices_file);
      std::vector<float> adj_close = prices_data.GetColumn<float>(field);
      prices[*iter] = adj_close;
   }
   return prices;
}

int main()
{
   /*
  // NOTE: set the working directory to same as the CSV file dir
  rapidcsv::Document doc("colhdr.csv");

  std::vector<float> col = doc.GetColumn<float>("Close");
  std::cout << "Read " << col.size() << " values." << std::endl;
  // display the values
  std::cout << "Here are the contents..." << std::endl;
  display_vector(col);

  // here we are reading a CSV where first col must be the row label
  // and first row the column headers
  rapidcsv::Document doc2("colrowhdr.csv", rapidcsv::LabelParams(0, 0));

  // read a row of data (Date, Open, High, Low, Close, Volume, Adj Close)
  std::vector<float> row = doc2.GetRow<float>("2017-02-22");
  std::cout << "Read " << row.size() << " values." << std::endl;
  // display the values
  std::cout << "Here are the contents..." << std::endl;
  display_vector(row);

  // get volume from same row
  long long volume = doc2.GetCell<long long>("Volume", "2017-02-22");
  std::cout << "Volume " << volume << " on 2017-02-22." << std::endl;
  */

   // load all prices from CSV files
   PricesMap prices = loadPrices();
   auto adj_close_reliance = prices["RELIANCE.NS"];
   display_vector(adj_close_reliance, "Values of Adj Close -> Reliance");

   // now let's do some real analysis

   /*
  rapidcsv::Document reliance("RELIANCE.NS.csv", rapidcsv::LabelParams(0, 0));
  std::vector<float> adj_close = reliance.GetColumn<float>("Adj Close");
  display_vector(adj_close, "Values of Adj Close");
  std::vector<long long> volume2 = reliance.GetColumn<long long>("Volume");
  display_vector(volume2, "Values of Volume");
  */

   double sum = std::accumulate(
         adj_close_reliance.cbegin(), adj_close_reliance.cend(), 0.0
   );
   auto mean_adj_close = sum / adj_close_reliance.size();
   std::cout << fmt::format("Mean Adj Close: {:.3f}", mean_adj_close) << std::endl;
   std::vector<float> ma_20 = fincalc::Equities<float>::ma(adj_close_reliance, 20);
   std::vector<float> ema_20 = fincalc::Equities<float>::ema(adj_close_reliance, 20);
   // fmt::print("Adj Close MA(20): {} elements -> {}\n", mas.size(), mas);
   fmt::print("Adj Close EMA(20): {} elements -> {}\n", ema_20.size(), ema_20);
   std::cout << fmt::format(
         "Ranges of Adj Close -> Overall: {:.3f} - Daily: "
         "{:.3f} - StdDev: {:.3f}",
         fincalc::Equities<float>::range(adj_close_reliance),
         fincalc::Equities<float>::avgDailyRange(adj_close_reliance),
         fincalc::Equities<float>::stdDev(adj_close_reliance)
   ) << std::endl;

   // find co-relation between prices
   // NOTE: stocks with a strong co-relation will move together (same direction)
   std::vector<float> adj_close_tcs = prices["TCS.NS"];
   std::vector<float> adj_close_persistent = prices["PERSISTENT.NS"];
   std::vector<float> adj_close_kansai = prices["KANSAINER.NS"];
   std::vector<float> adj_close_pidilite = prices["PIDILITIND.NS"];
   // should be 1.0
   double corr_tcs_tcs = fincalc::Equities<float>::corr(adj_close_tcs, adj_close_tcs);
   std::cout << fmt::format("Correl (TCS & TCS): {:.3f}", corr_tcs_tcs) << std::endl;
   double corr_tcs_persistent
         = fincalc::Equities<float>::corr(adj_close_tcs, adj_close_persistent);
   std::cout << fmt::format(
         "Correl (TCS & Persistent Systems): {:.3f}", corr_tcs_persistent
   ) << std::endl;
   double corr_tcs_reliance
         = fincalc::Equities<float>::corr(adj_close_tcs, adj_close_reliance);
   std::cout << fmt::format("Correl (TCS & Reliance Systems): {:.3f}", corr_tcs_reliance)
             << std::endl;
   double corr_kansai_pidilite
         = fincalc::Equities<float>::corr(adj_close_kansai, adj_close_pidilite);
   std::cout << fmt::format("Correl (Kansai & Pidilite): {:.3f}", corr_kansai_pidilite)
             << std::endl;

   // find corr of Nifty50 with other stocks in my portfolio
   std::vector<float> adj_close_nifty = prices["^NSEI"];

   std::map<std::string, float> corr_map;

   for (auto iter = prices.begin(); iter != prices.end(); ++iter) {
      if (iter->first != "^NSEI") {
         try {
            std::vector<float> adj_close = prices[iter->first];
            double corr = fincalc::Equities<float>::corr(adj_close_nifty, adj_close);
            corr_map[fmt::format("NIFTY-{}", iter->first)] = corr;
         }
         catch (const char *msg) {
            std::cerr << fmt::format(
                  "ERROR: {} - ignoring pair NIFTY-{}", msg, iter->first
            ) << std::endl;
         }
      }
   }

   // now display the corr-map sorted descending by corr
   std::cout << std::endl << "Corelation of NIFTY to portfolio stocks" << std::endl;
   std::cout << "---------------------------------------" << std::endl;
   std::vector<std::pair<std::string, float>> sorted_on_corr = sort_on_corr_desc(
         corr_map
   );
   for (auto &iter : sorted_on_corr)
      std::cout << fmt::format("{:<25} = {:.3f}\n", iter.first, iter.second);

   // if TCS & Reliance are co-related
}
