#include <algorithm>
#include <cmath>
#include <iostream>
#include <string>
#include <vector>

double delay_function(double u){
  if(u >= 1.0) return 999.0;
  return 1.0 * (1.0 + 0.8 * (u / (1.0 - u)));
}

int main(){
  std::vector<double> arrivals = {75.0, 95.0, 115.0};
  std::vector<std::string> names = {"baseline_spare_capacity","near_capacity_operation","over_capacity_backlog"};
  std::cout << "scenario_name,system_type,utilization,delay_warning\n";
  for(size_t i=0;i<arrivals.size();++i){
    double u = arrivals[i] / 100.0;
    std::cout << names[i] << ",queue_capacity," << u << "," << delay_function(std::min(u,0.999)) << "\n";
  }
}
