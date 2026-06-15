#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

double response_function(double x){ return 10.0 * std::sqrt(x + 1.0); }
double analytic_derivative(double x){ return 5.0 / std::sqrt(x + 1.0); }
double elasticity(double x){
  double y=response_function(x);
  if(x==0.0 || y==0.0) return std::numeric_limits<double>::quiet_NaN();
  return (x/y)*analytic_derivative(x);
}

int main(){
  std::vector<double> xs={0.0,0.5,1.0,4.0,9.0,24.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"x,value,derivative,elasticity\n";
  for(double x:xs){
    std::cout<<x<<","<<response_function(x)<<","<<analytic_derivative(x)<<","<<elasticity(x)<<"\n";
  }
}
