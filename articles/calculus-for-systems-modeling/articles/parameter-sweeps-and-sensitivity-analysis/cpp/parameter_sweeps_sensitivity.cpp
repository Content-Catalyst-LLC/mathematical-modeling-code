#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double logistic(double t, double x0, double r, double k){
  return k / (1.0 + ((k - x0) / x0) * std::exp(-r * t));
}
int main(){
  std::vector<double> rates{0.18, 0.25, 0.35, 0.45, 0.55};
  std::vector<double> caps{80.0, 100.0, 125.0, 150.0};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "growth_rate,carrying_capacity,initial_value,stop_time,final_value,output_metric,warning\n";
  for(double r : rates){
    for(double k : caps){
      std::cout << r << "," << k << ",10.000000000000,20.000000000000," << logistic(20.0, 10.0, r, k) << ",final_state_value,Sweep results depend on tested ranges baseline assumptions and model structure.\n";
    }
  }
}
