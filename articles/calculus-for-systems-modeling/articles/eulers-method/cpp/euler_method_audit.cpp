#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>

double exact_solution(double t, double y0, double k){
  return y0 * std::exp(-k * t);
}

int main(){
  const double y0 = 100.0, k = 0.35, h = 0.1, stop_time = 20.0;
  const int steps = static_cast<int>(std::round(stop_time / h));
  double y = y0;
  double multiplier = 1.0 - h * k;
  std::string status = std::abs(multiplier) <= 1.0 ? "stable_for_simple_decay" : "unstable_risk";

  std::cout << std::fixed << std::setprecision(12);
  std::cout << "step,time,euler_value,exact_value,absolute_error,step_size,stability_multiplier,stability_status,warning\n";
  for(int step=0; step<=steps; step++){
    double t = step * h;
    double exact = exact_solution(t, y0, k);
    std::cout << step << "," << t << "," << y << "," << exact << "," << std::abs(y - exact) << "," << h << "," << multiplier << "," << status << ",Euler estimates depend on time step rate function initial condition stability and accumulated error.\n";
    y = y + h * (-k * y);
  }
}
