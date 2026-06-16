#include <cmath>
#include <iomanip>
#include <iostream>

double rate_function(double, double y, double k){ return -k * y; }
double exact_solution(double t, double y0, double k){ return y0 * std::exp(-k * t); }
double euler_step(double t, double y, double h, double k){ return y + h * rate_function(t, y, k); }

double rk4_step(double t, double y, double h, double k){
  double k1 = rate_function(t, y, k);
  double k2 = rate_function(t + h/2.0, y + h*k1/2.0, k);
  double k3 = rate_function(t + h/2.0, y + h*k2/2.0, k);
  double k4 = rate_function(t + h, y + h*k3, k);
  return y + (h/6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4);
}

int main(){
  const double y0 = 100.0, k = 0.35, h = 0.5, stop_time = 20.0;
  const int steps = static_cast<int>(std::round(stop_time / h));
  double y_euler = y0, y_rk4 = y0;

  std::cout << std::fixed << std::setprecision(12);
  std::cout << "step,time,euler_value,rk4_value,exact_value,euler_absolute_error,rk4_absolute_error,step_size,warning\n";
  for(int step=0; step<=steps; step++){
    double t = step * h;
    double exact = exact_solution(t, y0, k);
    std::cout << step << "," << t << "," << y_euler << "," << y_rk4 << "," << exact << "," << std::abs(y_euler-exact) << "," << std::abs(y_rk4-exact) << "," << h << ",Runge-Kutta estimates depend on rate function step size smoothness stiffness and benchmark comparison.\n";
    y_euler = euler_step(t, y_euler, h, k);
    y_rk4 = rk4_step(t, y_rk4, h, k);
  }
}
