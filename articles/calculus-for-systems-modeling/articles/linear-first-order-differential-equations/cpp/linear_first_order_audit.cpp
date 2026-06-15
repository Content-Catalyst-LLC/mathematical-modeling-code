#include <cmath>
#include <iomanip>
#include <iostream>

double equilibrium(double input, double loss){ return input/loss; }
double rate_law(double y, double input, double loss){ return input - loss*y; }
double analytical(double t, double y0, double input, double loss){
  double eq = equilibrium(input, loss);
  return eq + (y0 - eq)*std::exp(-loss*t);
}

int main(){
  double y0 = 20.0, y = 20.0, input = 12.0, loss = 0.4, dt = 0.1, eq = equilibrium(input, loss);
  int steps = 100;
  std::cout << std::fixed << std::setprecision(6);
  std::cout << "scenario,time,analytical_state,euler_state,absolute_error,input_rate,loss_rate,equilibrium,initial_state,method,warning\n";
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    double a = analytical(t,y0,input,loss);
    std::cout << "input_loss_balance," << t << "," << a << "," << y << "," << std::abs(a-y) << "," << input << "," << loss << "," << eq << "," << y0 << ",analytical_vs_explicit_euler,Assumes constant input and proportional loss.\n";
    y = y + dt*rate_law(y,input,loss);
  }
}
