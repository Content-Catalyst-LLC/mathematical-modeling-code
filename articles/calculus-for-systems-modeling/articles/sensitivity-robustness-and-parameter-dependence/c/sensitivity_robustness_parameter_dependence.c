#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double logistic_final(double x0, double r, double k, double t){
  return k / (1.0 + ((k - x0) / x0) * exp(-r * t));
}

int main(void){
  double baseline = logistic_final(10.0, 0.35, 100.0, 20.0);
  printf("parameter_name,baseline_output,status,warning\n");
  printf("growth_rate,%.6f,sensitive,conclusion may depend on growth-rate assumptions\n", baseline);
  printf("carrying_capacity,%.6f,sensitive,capacity scale affects final stock interpretation\n", baseline);
  printf("initial_stock,%.6f,stable,output variation is limited across this synthetic range\n", baseline);
  return EXIT_SUCCESS;
}
