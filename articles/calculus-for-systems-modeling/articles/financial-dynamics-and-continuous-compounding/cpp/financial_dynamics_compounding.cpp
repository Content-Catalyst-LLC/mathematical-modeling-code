#include <cmath>
#include <iostream>

double continuous_future_value(double v0, double r, double t){
  return v0 * std::exp(r * t);
}

double continuous_present_value(double fv, double r, double t){
  return fv * std::exp(-r * t);
}

int main(){
  std::cout << "scenario_name,model_type,final_value,present_value,warning\n";
  std::cout << "continuous_compounding_case,future_value," << continuous_future_value(1000.0,0.05,30.0) << ",1000,continuous_compounding\n";
  std::cout << "discounted_future_value,present_value,5000," << continuous_present_value(5000.0,0.05,30.0) << ",discounting\n";
}
