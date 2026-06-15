#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double response_function(double x){ return 10.0 * sqrt(x + 1.0); }
double analytic_derivative(double x){ return 5.0 / sqrt(x + 1.0); }
double elasticity(double x){ double y=response_function(x); if(x==0.0 || y==0.0) return NAN; return (x/y)*analytic_derivative(x); }

int main(void){
  double xs[]={0.0,0.5,1.0,4.0,9.0,24.0};
  printf("x,value,derivative,elasticity\n");
  for(int i=0;i<6;i++){
    double x=xs[i];
    printf("%.6f,%.12f,%.12f,%.12f\n",x,response_function(x),analytic_derivative(x),elasticity(x));
  }
  return EXIT_SUCCESS;
}
