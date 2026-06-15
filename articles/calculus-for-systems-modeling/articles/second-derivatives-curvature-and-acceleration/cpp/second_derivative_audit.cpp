#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double logistic(double x){ return 1.0 / (1.0 + std::exp(-x)); }
double first_derivative(double x){ double y=logistic(x); return y*(1.0-y); }
double second_derivative(double x){ double y=logistic(x); return y*(1.0-y)*(1.0-2.0*y); }
double curvature_value(double x){ double fp=first_derivative(x); double fpp=second_derivative(x); return std::abs(fpp)/std::pow(1.0+fp*fp,1.5); }

int main(){
  std::vector<double> xs={-4.0,-2.0,-1.0,0.0,1.0,2.0,4.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"x,value,first_derivative,second_derivative,curvature\n";
  for(double x:xs){
    std::cout<<x<<","<<logistic(x)<<","<<first_derivative(x)<<","<<second_derivative(x)<<","<<curvature_value(x)<<"\n";
  }
}
