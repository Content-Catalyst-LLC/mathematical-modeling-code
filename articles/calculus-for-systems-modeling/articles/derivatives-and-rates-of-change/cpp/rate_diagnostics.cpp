#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

double system_response(double x){ return std::exp(0.2*x); }
double exact_derivative(double x){ return 0.2*std::exp(0.2*x); }
double average_rate(double a,double b){ return (system_response(b)-system_response(a))/(b-a); }
double forward_difference(double x,double h){ return (system_response(x+h)-system_response(x))/h; }
double backward_difference(double x,double h){ return (system_response(x)-system_response(x-h))/h; }
double central_difference(double x,double h){ return (system_response(x+h)-system_response(x-h))/(2.0*h); }
double elasticity(double d,double x){ return (x/system_response(x))*d; }

int main(){
  double x=5.0, exact=exact_derivative(x);
  std::vector<double> hs={1.0,0.5,0.25,0.125,0.0625};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"method,x0,h,estimate,exact,absolute_error,elasticity\n";
  for(double h:hs){
    std::vector<std::pair<std::string,double>> rows={
      {"average_rate_right",average_rate(x,x+h)},
      {"forward_difference",forward_difference(x,h)},
      {"backward_difference",backward_difference(x,h)},
      {"central_difference",central_difference(x,h)}
    };
    for(auto &r:rows){
      std::cout<<r.first<<","<<x<<","<<h<<","<<r.second<<","<<exact<<","<<std::fabs(r.second-exact)<<","<<elasticity(r.second,x)<<"\n";
    }
  }
}
