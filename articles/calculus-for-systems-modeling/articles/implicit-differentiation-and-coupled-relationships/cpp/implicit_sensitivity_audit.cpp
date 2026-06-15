#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double equilibrium_state(double p){ return (-p + std::sqrt(p*p + 40.0)) / 2.0; }
double constraint(double x, double p){ return x*x + p*x - 10.0; }
double partial_state(double x, double p){ return 2.0*x + p; }
double partial_parameter(double x, double){ return x; }
double implicit_sensitivity(double x, double p){ return -partial_parameter(x,p) / partial_state(x,p); }

int main(){
  std::vector<double> ps={-3.0,-1.0,0.0,1.0,3.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"parameter,equilibrium_state,constraint_value,partial_state,partial_parameter,implicit_sensitivity\n";
  for(double p:ps){
    double x=equilibrium_state(p), gx=partial_state(x,p), gp=partial_parameter(x,p), sens=implicit_sensitivity(x,p);
    std::cout<<p<<","<<x<<","<<constraint(x,p)<<","<<gx<<","<<gp<<","<<sens<<"\n";
  }
}
