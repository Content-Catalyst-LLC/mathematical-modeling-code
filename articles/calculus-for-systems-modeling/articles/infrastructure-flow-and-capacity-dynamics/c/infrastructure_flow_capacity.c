#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double delay_function(double u){
  if(u >= 1.0) return 999.0;
  return 1.0 * (1.0 + 0.8 * (u / (1.0 - u)));
}

int main(void){
  double arrivals[] = {75.0, 95.0, 115.0};
  const char* names[] = {"baseline_spare_capacity","near_capacity_operation","over_capacity_backlog"};
  printf("scenario_name,system_type,utilization,delay_warning\n");
  for(int i=0;i<3;i++){
    double u = arrivals[i] / 100.0;
    printf("%s,queue_capacity,%.6f,%.6f\n", names[i], u, delay_function(fmin(u,0.999)));
  }
  return EXIT_SUCCESS;
}
