#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

double forward_model(double x){ return log1p(x); }
double forward_derivative(double x){ return 1.0 / (1.0 + x); }
double inverse_model(double y){ return exp(y) - 1.0; }

int main(void){
  double ys[]={0.0,0.5,1.0,1.5,2.0};
  printf("target_output,recovered_input,forward_check,residual,forward_derivative,inverse_sensitivity,domain_valid\n");
  for(int i=0;i<5;i++){
    double y=ys[i], x=inverse_model(y), ycheck=forward_model(x), residual=ycheck-y;
    double derivative=forward_derivative(x), invsens=1.0/derivative;
    int domain_valid = x > -1.0;
    printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%d\n",y,x,ycheck,residual,derivative,invsens,domain_valid);
  }
  return EXIT_SUCCESS;
}
