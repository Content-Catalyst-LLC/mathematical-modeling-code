#include <cmath>
#include <iostream>

double r0_value(double beta, double gamma){
  return beta / gamma;
}
double doubling_time(double growth){
  return growth <= 0.0 ? INFINITY : std::log(2.0) / growth;
}

int main(){
  std::cout << "scenario_name,model_type,reproduction_number,doubling_time,warning\n";
  std::cout << "baseline_sir,SIR," << r0_value(0.32,0.10) << "," << doubling_time(0.22) << ",baseline_model_assumptions\n";
  std::cout << "reduced_transmission_sir,SIR," << r0_value(0.22,0.10) << "," << doubling_time(0.12) << ",reduced_transmission_must_have_mechanism\n";
}
