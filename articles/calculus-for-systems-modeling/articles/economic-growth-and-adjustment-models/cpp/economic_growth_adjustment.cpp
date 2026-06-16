#include <cmath>
#include <iostream>
#include <vector>

double exponential_output(double y0, double g, double t){
  return y0 * std::exp(g * t);
}

int main(){
  std::vector<double> rates = {0.01, 0.025, 0.04};
  std::cout << "scenario_name,model_type,growth_rate,final_output,doubling_time,warning\n";
  for(double g : rates){
    std::cout << "growth_rate_case,exponential_growth," << g << "," << exponential_output(100.0, g, 40.0) << "," << std::log(2.0)/g << ",growth_rate_assumptions_compound\n";
  }
}
