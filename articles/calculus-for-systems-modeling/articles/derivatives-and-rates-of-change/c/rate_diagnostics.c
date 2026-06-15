#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double system_response(double x){ return exp(0.2 * x); }
double exact_derivative(double x){ return 0.2 * exp(0.2 * x); }
double average_rate(double a,double b){ return (system_response(b)-system_response(a))/(b-a); }
double forward_difference(double x,double h){ return (system_response(x+h)-system_response(x))/h; }
double backward_difference(double x,double h){ return (system_response(x)-system_response(x-h))/h; }
double central_difference(double x,double h){ return (system_response(x+h)-system_response(x-h))/(2.0*h); }
double elasticity(double d,double x){ return (x/system_response(x))*d; }

int main(void){
  double x=5.0, exact=exact_derivative(x);
  double hs[]={1.0,0.5,0.25,0.125,0.0625};
  printf("method,x0,h,estimate,exact,absolute_error,elasticity\n");
  for(int i=0;i<5;i++){
    double h=hs[i];
    double estimates[]={average_rate(x,x+h),forward_difference(x,h),backward_difference(x,h),central_difference(x,h)};
    const char *methods[]={"average_rate_right","forward_difference","backward_difference","central_difference"};
    for(int j=0;j<4;j++){
      printf("%s,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f\n",methods[j],x,h,estimates[j],exact,fabs(estimates[j]-exact),elasticity(estimates[j],x));
    }
  }
  return EXIT_SUCCESS;
}
