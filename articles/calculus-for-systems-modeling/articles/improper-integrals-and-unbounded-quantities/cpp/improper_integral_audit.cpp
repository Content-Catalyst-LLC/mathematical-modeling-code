#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double tail_function(double x){ return std::exp(-0.4*x); }

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
  std::vector<double> cutoffs{2,4,8,12,20};
  double reference = 1.0/0.4;
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"cutoff,truncated_value,reference_value,tail_error\n";
  for(double cutoff: cutoffs){
    double truncated = trap(tail_function,0.0,cutoff,4000);
    double tail_error = reference - truncated;
    std::cout<<cutoff<<","<<truncated<<","<<reference<<","<<tail_error<<"\n";
  }
}
