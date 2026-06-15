#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double state_value(double t){ return 50.0 + 2.0 * t + 3.0 * std::sin(t); }
double rate_value(double t){ return 2.0 + 3.0 * std::cos(t); }

int main(){
  std::vector<double> times{0,0.25,0.5,0.75,1,1.25,1.5,1.75,2};
  double accumulated_rate = 0.0;

  for(size_t i=0;i+1<times.size();++i){
    double dt = times[i+1] - times[i];
    accumulated_rate += 0.5 * (rate_value(times[i]) + rate_value(times[i+1])) * dt;
  }

  double endpoint_difference = state_value(times.back()) - state_value(times.front());
  double residual = endpoint_difference - accumulated_rate;

  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"interval_start,interval_end,endpoint_difference,accumulated_rate,residual\n";
  std::cout<<times.front()<<","<<times.back()<<","<<endpoint_difference<<","<<accumulated_rate<<","<<residual<<"\n";
}
