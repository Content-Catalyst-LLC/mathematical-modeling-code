#include <iomanip>
#include <iostream>
#include <vector>

int main(){
  std::vector<double> duration{1,1,1,1,1};
  std::vector<double> inflow{12,10,9,8,7};
  std::vector<double> outflow{6,7,8,9,9};
  std::vector<double> exposure{20,18,15,13,11};
  std::vector<double> population{1000,1100,1050,980,960};

  double initial_stock = 50.0;
  double cumulative_in = 0.0, cumulative_out = 0.0, cumulative_exposure = 0.0, pop_exposure = 0.0;

  for(size_t i=0;i<duration.size();++i){
    cumulative_in += inflow[i]*duration[i];
    cumulative_out += outflow[i]*duration[i];
    cumulative_exposure += exposure[i]*duration[i];
    pop_exposure += exposure[i]*population[i]*duration[i];
  }

  double net = cumulative_in - cumulative_out;
  double ending_stock = initial_stock + net;
  double gross = cumulative_in + cumulative_out;

  std::cout<<std::fixed<<std::setprecision(6);
  std::cout<<"initial_stock,cumulative_inflow,cumulative_outflow,net_accumulation,ending_stock,cumulative_exposure,population_weighted_exposure,gross_activity\n";
  std::cout<<initial_stock<<","<<cumulative_in<<","<<cumulative_out<<","<<net<<","<<ending_stock<<","<<cumulative_exposure<<","<<pop_exposure<<","<<gross<<"\n";
}
