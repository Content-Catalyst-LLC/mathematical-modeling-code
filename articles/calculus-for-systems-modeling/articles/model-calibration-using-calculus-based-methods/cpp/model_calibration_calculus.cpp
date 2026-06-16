#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>
#include <algorithm>

double logistic(double t, double x0, double r, double k){
  return k / (1.0 + ((k - x0) / x0) * std::exp(-r * t));
}
int main(){
  std::vector<double> times{0,2,4,6,8,10,12};
  std::vector<double> observed{10.0,17.5,29.2,44.1,60.5,74.0,83.2};
  std::vector<double> rates{0.22,0.26,0.30,0.34,0.38,0.42};
  std::vector<double> caps{85.0,95.0,105.0,115.0,125.0};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "growth_rate,carrying_capacity,loss,mean_absolute_residual,max_absolute_residual,warning\n";
  for(double r : rates){
    for(double k : caps){
      double loss=0.0, abs_sum=0.0, max_abs=0.0;
      for(size_t n=0; n<times.size(); ++n){
        double pred = logistic(times[n], 10.0, r, k);
        double res = observed[n] - pred;
        double ar = std::abs(res);
        loss += res*res;
        abs_sum += ar;
        max_abs = std::max(max_abs, ar);
      }
      std::cout << r << "," << k << "," << loss << "," << abs_sum/times.size() << "," << max_abs << ",Calibration fit does not prove model validity validation and sensitivity review remain required.\n";
    }
  }
}
