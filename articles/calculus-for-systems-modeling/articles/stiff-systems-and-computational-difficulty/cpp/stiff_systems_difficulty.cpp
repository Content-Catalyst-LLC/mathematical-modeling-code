#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double exact_solution(double t, double y0, double lambda){ return y0 * std::exp(lambda * t); }
double explicit_value(double y0, double lambda, double h, double stop_time){
  int steps = static_cast<int>(std::round(stop_time / h));
  double amp = 1.0 + h * lambda;
  double y = y0;
  for(int i=0; i<steps; ++i) y *= amp;
  return y;
}
double implicit_value(double y0, double lambda, double h, double stop_time){
  int steps = static_cast<int>(std::round(stop_time / h));
  double amp = 1.0 / (1.0 - h * lambda);
  double y = y0;
  for(int i=0; i<steps; ++i) y *= amp;
  return y;
}
int main(){
  double y0 = 1.0, lambda = -50.0, stop_time = 1.0;
  double exact_final = exact_solution(stop_time, y0, lambda);
  std::vector<double> hs{0.1, 0.05, 0.025, 0.01};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "step_size,eigenvalue,method,amplification_factor,stability_status,final_value,exact_final_value,absolute_error,warning\n";
  for(double h : hs){
    double ev = explicit_value(y0, lambda, h, stop_time);
    double eamp = std::abs(1.0 + h * lambda);
    double iv = implicit_value(y0, lambda, h, stop_time);
    double iamp = std::abs(1.0 / (1.0 - h * lambda));
    std::cout << h << "," << lambda << ",explicit_euler," << eamp << "," << (eamp <= 1.0 ? "stable_for_test_problem" : "unstable_for_test_problem") << "," << ev << "," << exact_final << "," << std::abs(ev-exact_final) << ",Explicit methods may require very small steps on stiff systems.\n";
    std::cout << h << "," << lambda << ",implicit_euler," << iamp << "," << (iamp <= 1.0 ? "stable_for_test_problem" : "unstable_for_test_problem") << "," << iv << "," << exact_final << "," << std::abs(iv-exact_final) << ",Implicit stability does not remove accuracy review.\n";
  }
}
