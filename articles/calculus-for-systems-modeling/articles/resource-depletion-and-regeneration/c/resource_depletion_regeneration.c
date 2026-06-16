#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double logistic_regeneration(double stock, double r, double k){
  double v = r * stock * (1.0 - stock / k);
  return v > 0.0 ? v : 0.0;
}

int main(void){
  double stock=600.0, harvest=35.0, dt=0.1, extraction, growth, cumulative=0.0;
  for(int i=0;i<800;i++){
    extraction = fmin(stock, harvest * dt);
    growth = logistic_regeneration(stock, 0.18, 1000.0) * dt;
    stock = fmax(0.0, stock + growth - extraction);
    cumulative += extraction;
  }
  printf("scenario_name,resource_type,final_stock,cumulative_extraction,warning\n");
  printf("renewable_precautionary_harvest,renewable_logistic,%.6f,%.6f,precautionary_harvest\n", stock, cumulative);
  return EXIT_SUCCESS;
}
