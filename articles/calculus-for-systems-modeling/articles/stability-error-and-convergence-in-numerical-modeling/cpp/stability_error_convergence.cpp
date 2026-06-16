#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double exact_solution(double t, double y0, double k){ return y0 * std::exp(-k * t); }
double rate_function(double, double y, double k){ return -k * y; }
double rk4_step(double t, double y, double h, double k){
  double k1 = rate_function(t, y, k);
  double k2 = rate_function(t + h/2.0, y + h*k1/2.0, k);
  double k3 = rate_function(t + h/2.0, y + h*k2/2.0, k);
  double k4 = rate_function(t + h, y + h*k3, k);
  return y + (h/6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4);
}
double simulate(double y0, double k, double h, double stop_time){
  int steps = static_cast<int>(std::round(stop_time / h));
  double y = y0;
  for(int step=0; step<steps; ++step) y = rk4_step(step*h, y, h, k);
  return y;
}
int main(){
  double y0 = 100.0, k = 0.35, stop_time = 20.0;
  double exact_final = exact_solution(stop_time, y0, k);
  std::vector<double> hs{1.0, 0.5, 0.25, 0.125};
  std::cout << std::fixed << std::setprecision(12);
  std::cout << "step_size,steps,solver_method,final_numeric_value,final_exact_value,final_absolute_error,warning\n";
  for(double h : hs){
    double numeric = simulate(y0, k, h, stop_time);
    std::cout << h << "," << static_cast<int>(std::round(stop_time / h)) << ",fixed_step_rk4," << numeric << "," << exact_final << "," << std::abs(numeric-exact_final) << ",Convergence evidence supports numerical reliability not empirical validity.\n";
  }
}
