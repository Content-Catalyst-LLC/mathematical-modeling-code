#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double emissions(double t){ return 50.0 * std::exp(0.015 * t); }
double emissions_rate(double t){ return 0.015 * emissions(t); }
double concentration(double e){ return 0.5 * e; }
double d_concentration_d_emissions(double){ return 0.5; }
double forcing(double c){ return std::log(1.0 + c); }
double d_forcing_d_concentration(double c){ return 1.0 / (1.0 + c); }
double temperature_response(double f){ return 1.2 * f; }
double d_temperature_d_forcing(double){ return 1.2; }

int main(){
  std::vector<double> ts={0.0,5.0,10.0,20.0,40.0};
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"t,emissions,concentration,forcing,temperature,emissions_rate,d_concentration_d_emissions,d_forcing_d_concentration,d_temperature_d_forcing,total_derivative\n";
  for(double t:ts){
    double e=emissions(t), c=concentration(e), f=forcing(c), temp=temperature_response(f);
    double s1=emissions_rate(t), s2=d_concentration_d_emissions(e), s3=d_forcing_d_concentration(c), s4=d_temperature_d_forcing(f);
    std::cout<<t<<","<<e<<","<<c<<","<<f<<","<<temp<<","<<s1<<","<<s2<<","<<s3<<","<<s4<<","<<s4*s3*s2*s1<<"\n";
  }
}
