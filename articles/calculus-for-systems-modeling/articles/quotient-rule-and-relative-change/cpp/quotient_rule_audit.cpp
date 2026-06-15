#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double resource(double t){ return 1000.0 * std::exp(-0.01*t); }
double resource_rate(double t){ return -0.01 * resource(t); }
double population(double t){ return 100.0 * std::exp(0.02*t); }
double population_rate(double t){ return 0.02 * population(t); }

int main(){
  std::vector<double> ts={0.0,5.0,10.0,20.0,40.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"t,numerator,denominator,ratio,numerator_rate,denominator_rate,numerator_effect,denominator_effect,quotient_derivative,ratio_relative_rate\n";
  for(double t:ts){
    double f=resource(t), g=population(t), fp=resource_rate(t), gp=population_rate(t);
    double ratio=f/g, ne=fp/g, de=-(f*gp)/(g*g), qd=ne+de;
    std::cout<<t<<","<<f<<","<<g<<","<<ratio<<","<<fp<<","<<gp<<","<<ne<<","<<de<<","<<qd<<","<<qd/ratio<<"\n";
  }
}
