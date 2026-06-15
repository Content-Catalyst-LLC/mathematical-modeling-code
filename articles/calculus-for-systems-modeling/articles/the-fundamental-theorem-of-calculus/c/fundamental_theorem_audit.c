#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double state_value(double t){ return 50.0 + 2.0 * t + 3.0 * sin(t); }
double rate_value(double t){ return 2.0 + 3.0 * cos(t); }

int main(void){
  double times[] = {0,0.25,0.5,0.75,1,1.25,1.5,1.75,2};
  double accumulated_rate = 0.0;

  for(int i=0;i<8;i++){
    double dt = times[i+1] - times[i];
    accumulated_rate += 0.5 * (rate_value(times[i]) + rate_value(times[i+1])) * dt;
  }

  double endpoint_difference = state_value(times[8]) - state_value(times[0]);
  double residual = endpoint_difference - accumulated_rate;

  printf("interval_start,interval_end,endpoint_difference,accumulated_rate,residual\n");
  printf("%.6f,%.6f,%.12f,%.12f,%.12f\n", times[0], times[8], endpoint_difference, accumulated_rate, residual);
  return EXIT_SUCCESS;
}
