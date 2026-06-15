#include <cmath>
#include <iomanip>
#include <iostream>

double u_value(double x){ return 1.0 + x; }
double u_prime(double){ return 1.0; }
double v_value(double x){ return std::exp(-0.3*x) * std::sin(x); }
double v_prime(double x){ return std::exp(-0.3*x) * (std::cos(x) - 0.3*std::sin(x)); }
double direct_integrand(double x){ return u_value(x) * v_prime(x); }
double residual_integrand(double x){ return v_value(x) * u_prime(x); }

template <typename F>
double trap(F func, double a, double b, int n){
  double total = 0.0;
  double dx = (b-a)/n;
  for(int i=0;i<n;i++){
    double x0 = a + dx*i;
    double x1 = x0 + dx;
    total += 0.5*(func(x0)+func(x1))*dx;
  }
  return total;
}

int main(){
  double a = 0.0, b = 4.0;
  int n = 800;
  double direct = trap(direct_integrand, a, b, n);
  double residual = trap(residual_integrand, a, b, n);
  double boundary = u_value(b)*v_value(b) - u_value(a)*v_value(a);
  double decomposed = boundary - residual;
  double decomp_resid = direct - decomposed;

  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"interval_start,interval_end,direct_integral,boundary_term,residual_integral,decomposed_value,decomposition_residual\n";
  std::cout<<a<<","<<b<<","<<direct<<","<<boundary<<","<<residual<<","<<decomposed<<","<<decomp_resid<<"\n";
}
