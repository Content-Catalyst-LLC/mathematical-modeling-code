#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double logistic_derivative(double x, double growth, double carrying){ return growth*(1.0 - 2.0*x/carrying); }
double bistable_rate(double x, double threshold){ return x*(1.0-x)*(x-threshold); }
double numerical_derivative(double x, double threshold){
  double h = 1e-5;
  return (bistable_rate(x+h, threshold) - bistable_rate(x-h, threshold))/(2.0*h);
}
std::string classify(double d){
  if(d < -1e-8) return "locally_stable";
  if(d > 1e-8) return "locally_unstable";
  return "inconclusive_by_linearization";
}
int main(){
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "scenario,equilibrium,derivative_value,stability,domain_min,domain_max,warning\n";
  for(double eq : std::vector<double>{0.0, 100.0}){
    double d = logistic_derivative(eq, 0.6, 100.0);
    std::cout << "logistic_growth," << eq << "," << d << "," << classify(d) << ",0.000000,100.000000,Logistic stability assumes fixed carrying capacity and smooth density limitation.\n";
  }
  for(double eq : std::vector<double>{0.0, 0.4, 1.0}){
    double d = numerical_derivative(eq, 0.4);
    std::cout << "bistable_threshold," << eq << "," << d << "," << classify(d) << ",0.000000,1.000000,Threshold stability depends on the assumed threshold and domain.\n";
  }
}
