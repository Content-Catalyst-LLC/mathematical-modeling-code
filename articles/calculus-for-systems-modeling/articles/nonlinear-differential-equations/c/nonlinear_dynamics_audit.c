#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double logistic_rate(double x, double growth, double carrying){ return growth*x*(1.0 - x/carrying); }
double bistable_rate(double x, double threshold){ return x*(1.0-x)*(x-threshold); }

void simulate_logistic(void){
  double x = 10.0, dt = 0.05, growth = 0.6, carrying = 100.0;
  for(int n=0; n<=300; n++){
    double t = n*dt;
    double r = logistic_rate(x, growth, carrying);
    printf("logistic_growth,%.6f,%.6f,%.6f,%.6f,%.6f,0.000000,explicit_euler,Logistic growth assumes a fixed carrying capacity and smooth density limitation.\n", t, x, r, growth, carrying);
    x = x + dt*r;
  }
}

void simulate_threshold(void){
  double x = 0.35, dt = 0.05, threshold = 0.4;
  for(int n=0; n<=300; n++){
    double t = n*dt;
    double r = bistable_rate(x, threshold);
    printf("bistable_threshold,%.6f,%.6f,%.6f,%.6f,0.000000,0.000000,explicit_euler,Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.\n", t, x, r, threshold);
    x = x + dt*r;
  }
}

int main(void){
  printf("scenario,time,state,rate,parameter_a,parameter_b,parameter_c,method,warning\n");
  simulate_logistic();
  simulate_threshold();
  return EXIT_SUCCESS;
}
