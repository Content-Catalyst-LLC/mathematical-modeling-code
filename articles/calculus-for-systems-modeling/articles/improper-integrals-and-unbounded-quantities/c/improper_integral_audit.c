#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double tail_function(double x){ return exp(-0.4*x); }

double trap(double (*func)(double), double a, double b, int n){
  double total = 0.0;
  double dx = (b-a)/n;
  for(int i=0;i<n;i++){
    double x0 = a + dx*i;
    double x1 = x0 + dx;
    total += 0.5*(func(x0)+func(x1))*dx;
  }
  return total;
}

int main(void){
  double cutoffs[] = {2,4,8,12,20};
  double reference = 1.0/0.4;
  printf("cutoff,truncated_value,reference_value,tail_error\n");
  for(int i=0;i<5;i++){
    double cutoff = cutoffs[i];
    double truncated = trap(tail_function,0.0,cutoff,4000);
    double tail_error = reference - truncated;
    printf("%.6f,%.12f,%.12f,%.12f\n",cutoff,truncated,reference,tail_error);
  }
  return EXIT_SUCCESS;
}
