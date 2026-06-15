#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double logistic_derivative(double x, double growth, double carrying){ return growth*(1.0 - 2.0*x/carrying); }
double bistable_rate(double x, double threshold){ return x*(1.0-x)*(x-threshold); }
double numerical_derivative(double (*f)(double, double), double x, double parameter){
  double h = 1e-5;
  return (f(x+h, parameter) - f(x-h, parameter))/(2.0*h);
}
const char* classify(double d){
  if(d < -1e-8) return "locally_stable";
  if(d > 1e-8) return "locally_unstable";
  return "inconclusive_by_linearization";
}
int main(void){
  printf("scenario,equilibrium,derivative_value,stability,domain_min,domain_max,warning\n");
  double logistic_eqs[2] = {0.0, 100.0};
  for(int i=0; i<2; i++){
    double eq = logistic_eqs[i];
    double d = logistic_derivative(eq, 0.6, 100.0);
    printf("logistic_growth,%.6f,%.6f,%s,0.000000,100.000000,Logistic stability assumes fixed carrying capacity and smooth density limitation.\n", eq, d, classify(d));
  }
  double threshold = 0.4;
  double bistable_eqs[3] = {0.0, 0.4, 1.0};
  for(int i=0; i<3; i++){
    double eq = bistable_eqs[i];
    double d = numerical_derivative(bistable_rate, eq, threshold);
    printf("bistable_threshold,%.6f,%.6f,%s,0.000000,1.000000,Threshold stability depends on the assumed threshold and domain.\n", eq, d, classify(d));
  }
  return EXIT_SUCCESS;
}
