#include <cmath>
#include <iomanip>
#include <iostream>

double g_value(double x){ return x*x + 1.0; }
double g_prime(double x){ return 2.0*x; }
double f_value(double u){ return std::sqrt(u); }
double integrand_x(double x){ return f_value(g_value(x))*g_prime(x); }

template <typename F>
double trap(F func, double a, double b, int n){
  double total = 0.0;
  double step = (b-a)/n;
  for(int i=0;i<n;i++){
    double x0 = a + step*i;
    double x1 = x0 + step;
    total += 0.5*(func(x0)+func(x1))*step;
  }
  return total;
}

int main(){
  double a = 1.0, b = 3.0;
  double ua = g_value(a), ub = g_value(b);
  int n = 400;
  double direct = trap(integrand_x, a, b, n);
  double transformed = trap(f_value, ua, ub, n);
  double residual = direct - transformed;

  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"original_start,original_end,transformed_start,transformed_end,direct_integral,transformed_integral,residual\n";
  std::cout<<a<<","<<b<<","<<ua<<","<<ub<<","<<direct<<","<<transformed<<","<<residual<<"\n";
}
