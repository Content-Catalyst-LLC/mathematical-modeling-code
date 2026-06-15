#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double u_value(double x){ return 1.0 + x; }
double u_prime(double x){ (void)x; return 1.0; }
double v_value(double x){ return exp(-0.3*x) * sin(x); }
double v_prime(double x){ return exp(-0.3*x) * (cos(x) - 0.3*sin(x)); }
double direct_integrand(double x){ return u_value(x) * v_prime(x); }
double residual_integrand(double x){ return v_value(x) * u_prime(x); }

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
  double a = 0.0, b = 4.0;
  int n = 800;
  double direct = trap(direct_integrand, a, b, n);
  double residual = trap(residual_integrand, a, b, n);
  double boundary = u_value(b)*v_value(b) - u_value(a)*v_value(a);
  double decomposed = boundary - residual;
  double decomp_resid = direct - decomposed;

  printf("interval_start,interval_end,direct_integral,boundary_term,residual_integral,decomposed_value,decomposition_residual\n");
  printf("%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n",a,b,direct,boundary,residual,decomposed,decomp_resid);
  return EXIT_SUCCESS;
}
