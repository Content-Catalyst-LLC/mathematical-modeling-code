#include <cmath>
#include <iomanip>
#include <iostream>
#include <vector>

double net_rate(double t){ return 4.0 * std::sin(t / 2.0) + 1.0; }

int main(){
  std::vector<double> times{0,0.5,1,1.5,2,2.5,3,3.5,4};
  double signed_accumulation = 0.0;
  double absolute_accumulation = 0.0;

  for(size_t i=0;i+1<times.size();++i){
    double dt = times[i+1] - times[i];
    double r0 = net_rate(times[i]);
    double r1 = net_rate(times[i+1]);
    signed_accumulation += 0.5 * (r0 + r1) * dt;
    absolute_accumulation += 0.5 * (std::abs(r0) + std::abs(r1)) * dt;
  }

  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"interval_start,interval_end,method,signed_accumulation,absolute_accumulation\n";
  std::cout<<times.front()<<","<<times.back()<<",trapezoidal approximation,"<<signed_accumulation<<","<<absolute_accumulation<<"\n";
}
