#include <iomanip>
#include <iostream>
#include <vector>

double net_flow(double t){ return (12.0 + 0.5*t) - (7.0 + 0.2*t); }

int main(){
  std::vector<double> times{0,1,2,3,4,5,6};
  double stock = 100.0;
  std::cout<<std::fixed<<std::setprecision(12);
  std::cout<<"time,net_flow,recovered_stock,method\n";
  std::cout<<times[0]<<","<<net_flow(times[0])<<","<<stock<<",initial condition\n";
  for(size_t i=1;i<times.size();++i){
    double previous = times[i-1];
    double current = times[i];
    double dt = current - previous;
    stock += 0.5 * (net_flow(previous) + net_flow(current)) * dt;
    std::cout<<current<<","<<net_flow(current)<<","<<stock<<",trapezoidal accumulation\n";
  }
}
