#include <algorithm>
#include <cmath>
#include <iostream>

double logistic_regeneration(double stock, double r, double k){
  return std::max(0.0, r * stock * (1.0 - stock / k));
}

int main(){
  double stock=600.0, harvest=35.0, dt=0.1, cumulative=0.0;
  for(int i=0;i<800;i++){
    double extraction = std::min(stock, harvest * dt);
    double growth = logistic_regeneration(stock, 0.18, 1000.0) * dt;
    stock = std::max(0.0, stock + growth - extraction);
    cumulative += extraction;
  }
  std::cout << "scenario_name,resource_type,final_stock,cumulative_extraction,warning\n";
  std::cout << "renewable_precautionary_harvest,renewable_logistic," << stock << "," << cumulative << ",precautionary_harvest\n";
}
