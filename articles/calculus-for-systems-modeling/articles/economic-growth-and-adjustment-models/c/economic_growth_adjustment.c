#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double exponential_output(double y0, double g, double t){
  return y0 * exp(g * t);
}

int main(void){
  double rates[] = {0.01, 0.025, 0.04};
  printf("scenario_name,model_type,growth_rate,final_output,doubling_time,warning\n");
  for(int i=0;i<3;i++){
    double g = rates[i];
    printf("growth_rate_case,exponential_growth,%.6f,%.6f,%.6f,growth_rate_assumptions_compound\n", g, exponential_output(100.0, g, 40.0), log(2.0)/g);
  }
  return EXIT_SUCCESS;
}
