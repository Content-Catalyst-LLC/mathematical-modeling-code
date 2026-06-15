#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double g_value(double x){ return x*x + 1.0; }
double g_prime(double x){ return 2.0*x; }
double f_value(double u){ return sqrt(u); }
double integrand_x(double x){ return f_value(g_value(x))*g_prime(x); }

double trap(double (*func)(double), double a, double b, int n){
  double total = 0.0;
  double step = (b-a)/n;
  for(int i=0;i<n;i++){
    double x0 = a + step*i;
    double x1 = x0 + step;
    total += 0.5*(func(x0)+func(x1))*step;
  }
  return total;
}

int main(void){
  double a = 1.0, b = 3.0;
  double ua = g_value(a), ub = g_value(b);
  int n = 400;
  double direct = trap(integrand_x, a, b, n);
  double transformed = trap(f_value, ua, ub, n);
  double residual = direct - transformed;
  printf("original_start,original_end,transformed_start,transformed_end,direct_integral,transformed_integral,residual\n");
  printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f\n", a,b,ua,ub,direct,transformed,residual);
  return EXIT_SUCCESS;
}
