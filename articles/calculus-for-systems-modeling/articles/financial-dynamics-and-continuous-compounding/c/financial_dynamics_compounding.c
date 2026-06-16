#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double continuous_future_value(double v0, double r, double t){
  return v0 * exp(r * t);
}

double continuous_present_value(double fv, double r, double t){
  return fv * exp(-r * t);
}

int main(void){
  printf("scenario_name,model_type,final_value,present_value,warning\n");
  printf("continuous_compounding_case,future_value,%.6f,1000.000000,continuous_compounding\n", continuous_future_value(1000.0,0.05,30.0));
  printf("discounted_future_value,present_value,5000.000000,%.6f,discounting\n", continuous_present_value(5000.0,0.05,30.0));
  return EXIT_SUCCESS;
}
