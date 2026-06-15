#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>

double forcing_function(double t, double amplitude, double frequency){ return amplitude*std::cos(frequency*t); }

double acceleration(double x, double v, double t, double damping, double natural, double force_amp, double force_freq){
  double force = forcing_function(t, force_amp, force_freq);
  double damping_term = 2.0*damping*natural*v;
  double restoring = natural*natural*x;
  return force - damping_term - restoring;
}

void simulate(const std::string& scenario, double damping, double force_amp){
  double x = 1.0, v = 0.0, natural = 1.0, force_freq = 1.0, dt = 0.02;
  int steps = 500;
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    double a = acceleration(x, v, t, damping, natural, force_amp, force_freq);
    double force = forcing_function(t, force_amp, force_freq);
    std::cout << scenario << "," << t << "," << x << "," << v << "," << a << ","
              << damping << "," << natural << "," << force
              << ",explicit_euler_first_order_system,Explicit Euler is transparent but can distort oscillatory systems if the step size is too large.\n";
    v = v + dt*a;
    x = x + dt*v;
  }
}

int main(){
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "scenario,time,position,velocity,acceleration,damping_ratio,natural_frequency,forcing,method,warning\n";
  simulate("underdamped_unforced", 0.2, 0.0);
  simulate("forced_near_resonance", 0.1, 0.2);
}
