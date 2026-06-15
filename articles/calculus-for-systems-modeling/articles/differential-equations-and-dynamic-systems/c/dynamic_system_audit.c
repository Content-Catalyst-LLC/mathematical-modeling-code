#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double exponential_rate(double x, double r){ return r*x; }
double logistic_rate(double x, double r, double k){ return r*x*(1.0 - x/k); }

void simulate(const char* scenario, int logistic){
  double x = 10.0;
  double r = 0.35;
  double k = 100.0;
  double dt = 0.1;
  int steps = 100;
  for(int n=0; n<=steps; n++){
    double t = n*dt;
    double rate = logistic ? logistic_rate(x,r,k) : exponential_rate(x,r);
    printf("%s,%s,%.6f,%.6f,%.6f,%.6f,%.6f,%s,%s\n",
      scenario,
      logistic ? "dx_dt_equals_r_x_one_minus_x_over_K" : "dx_dt_equals_r_x",
      t, x, rate, r, logistic ? k : -1.0, "explicit_euler",
      logistic ? "Logistic growth assumes a fixed carrying capacity." : "Exponential growth assumes no capacity constraint.");
    x = x + dt*rate;
  }
}

int main(void){
  printf("scenario,model_type,time,state,rate,growth_rate,carrying_capacity,method,warning\n");
  simulate("exponential_growth", 0);
  simulate("logistic_growth", 1);
  return EXIT_SUCCESS;
}
