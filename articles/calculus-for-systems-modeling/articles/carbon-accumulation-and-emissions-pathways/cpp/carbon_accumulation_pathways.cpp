#include <algorithm>
#include <cmath>
#include <iostream>

double linear_decline(double e0, int year, int years){
  return std::max(0.0, e0 * (1.0 - static_cast<double>(year) / static_cast<double>(years)));
}

int main(){
  double e0 = 40.0;
  int years = 30;
  double cumulative = 0.0;
  for(int y=0; y<=years; ++y) cumulative += linear_decline(e0, y, years);
  std::cout << "scenario_name,pathway_type,cumulative_emissions,warning\n";
  std::cout << "linear_decline_to_zero,linear_decline," << cumulative << ",linear_decline_still_accumulates_until_net_zero\n";
}
