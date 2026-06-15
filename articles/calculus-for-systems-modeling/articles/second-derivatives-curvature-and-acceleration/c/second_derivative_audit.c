#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double logistic(double x){ return 1.0 / (1.0 + exp(-x)); }
double first_derivative(double x){ double y=logistic(x); return y*(1.0-y); }
double second_derivative(double x){ double y=logistic(x); return y*(1.0-y)*(1.0-2.0*y); }
double curvature_value(double x){ double fp=first_derivative(x); double fpp=second_derivative(x); return fabs(fpp)/pow(1.0+fp*fp,1.5); }

int main(void){
  double xs[]={-4.0,-2.0,-1.0,0.0,1.0,2.0,4.0};
  printf("x,value,first_derivative,second_derivative,curvature\n");
  for(int i=0;i<7;i++){
    double x=xs[i];
    printf("%.6f,%.12f,%.12f,%.12f,%.12f\n",x,logistic(x),first_derivative(x),second_derivative(x),curvature_value(x));
  }
  return EXIT_SUCCESS;
}
