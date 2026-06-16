#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double logistic(double t, double x0, double r, double k){
  return k / (1.0 + ((k - x0) / x0) * exp(-r * t));
}
int main(void){
  const double rates[5] = {0.18, 0.25, 0.35, 0.45, 0.55};
  const double caps[4] = {80.0, 100.0, 125.0, 150.0};
  printf("growth_rate,carrying_capacity,initial_value,stop_time,final_value,output_metric,warning\n");
  for(int i=0; i<5; i++){
    for(int j=0; j<4; j++){
      double v = logistic(20.0, 10.0, rates[i], caps[j]);
      printf("%.6f,%.6f,10.000000,20.000000,%.12f,final_state_value,Sweep results depend on tested ranges baseline assumptions and model structure.\n", rates[i], caps[j], v);
    }
  }
  return EXIT_SUCCESS;
}
