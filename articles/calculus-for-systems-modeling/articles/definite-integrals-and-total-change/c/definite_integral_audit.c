#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double net_rate(double t){ return 4.0 * sin(t / 2.0) + 1.0; }

int main(void){
  double times[] = {0,0.5,1,1.5,2,2.5,3,3.5,4};
  double signed_accumulation = 0.0;
  double absolute_accumulation = 0.0;

  for(int i=0;i<8;i++){
    double dt = times[i+1] - times[i];
    double r0 = net_rate(times[i]);
    double r1 = net_rate(times[i+1]);
    signed_accumulation += 0.5 * (r0 + r1) * dt;
    absolute_accumulation += 0.5 * (fabs(r0) + fabs(r1)) * dt;
  }

  printf("interval_start,interval_end,method,signed_accumulation,absolute_accumulation\n");
  printf("%.6f,%.6f,trapezoidal approximation,%.12f,%.12f\n", times[0], times[8], signed_accumulation, absolute_accumulation);
  return EXIT_SUCCESS;
}
