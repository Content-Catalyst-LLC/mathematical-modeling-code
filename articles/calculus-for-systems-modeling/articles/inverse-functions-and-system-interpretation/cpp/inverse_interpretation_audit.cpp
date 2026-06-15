#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double forward_model(double x){ return std::log1p(x); }
double forward_derivative(double x){ return 1.0 / (1.0 + x); }
double inverse_model(double y){ return std::exp(y) - 1.0; }

int main(){
  std::vector<double> ys={0.0,0.5,1.0,1.5,2.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"target_output,recovered_input,forward_check,residual,forward_derivative,inverse_sensitivity,domain_valid\n";
  for(double y:ys){
    double x=inverse_model(y), ycheck=forward_model(x), residual=ycheck-y;
    double derivative=forward_derivative(x), invsens=1.0/derivative;
    bool domain_valid=x > -1.0;
    std::cout<<y<<","<<x<<","<<ycheck<<","<<residual<<","<<derivative<<","<<invsens<<","<<domain_valid<<"\n";
  }
}
