#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double equilibrium(double input, double loss){ return input/loss; }
double rate_law(double y, double input, double loss){ return input - loss*y; }
double analytical(double t, double y0, double input, double loss){
  double eq = equilibrium(input, loss);
  return eq + (y0 - eq)*exp(-loss*t);
}

int main(void){
  double y0 = 20.0, y = 20.0, input = 12.0, loss = 0.4, dt = 0.1, eq = equilibrium(input, loss);
  int steps = 100;
  printf("scenario,time,analytical_state,euler_state,absolute_error,input_rate,loss_rate,equilibrium,initial_state,method,warning\n");
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    double a = analytical(t,y0,input,loss);
    printf("input_loss_balance,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,analytical_vs_explicit_euler,Assumes constant input and proportional loss.\n",
      t, a, y, fabs(a-y), input, loss, eq, y0);
    y = y + dt*rate_law(y,input,loss);
  }
  return EXIT_SUCCESS;
}
