#include <stdio.h>
#include <stdlib.h>

int main(void){
  double duration[5] = {1,1,1,1,1};
  double inflow[5] = {12,10,9,8,7};
  double outflow[5] = {6,7,8,9,9};
  double exposure[5] = {20,18,15,13,11};
  double population[5] = {1000,1100,1050,980,960};
  double initial_stock = 50.0;
  double cumulative_in = 0.0, cumulative_out = 0.0, cumulative_exposure = 0.0, pop_exposure = 0.0;

  for(int i=0;i<5;i++){
    cumulative_in += inflow[i]*duration[i];
    cumulative_out += outflow[i]*duration[i];
    cumulative_exposure += exposure[i]*duration[i];
    pop_exposure += exposure[i]*population[i]*duration[i];
  }

  double net = cumulative_in - cumulative_out;
  double ending_stock = initial_stock + net;
  double gross = cumulative_in + cumulative_out;

  printf("initial_stock,cumulative_inflow,cumulative_outflow,net_accumulation,ending_stock,cumulative_exposure,population_weighted_exposure,gross_activity\n");
  printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",initial_stock,cumulative_in,cumulative_out,net,ending_stock,cumulative_exposure,pop_exposure,gross);
  return EXIT_SUCCESS;
}
