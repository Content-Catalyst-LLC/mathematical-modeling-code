#include <math.h>
#include <stdio.h>
#include <stdlib.h>

static double logistic(double t, double x0, double r, double k){
  return k / (1.0 + ((k - x0) / x0) * exp(-r * t));
}
int main(void){
  double times[7] = {0,2,4,6,8,10,12};
  double observed[7] = {10.0,17.5,29.2,44.1,60.5,74.0,83.2};
  double rates[6] = {0.22,0.26,0.30,0.34,0.38,0.42};
  double caps[5] = {85.0,95.0,105.0,115.0,125.0};
  printf("growth_rate,carrying_capacity,loss,mean_absolute_residual,max_absolute_residual,warning\n");
  for(int i=0; i<6; i++){
    for(int j=0; j<5; j++){
      double loss=0, abs_sum=0, max_abs=0;
      for(int n=0; n<7; n++){
        double pred = logistic(times[n], 10.0, rates[i], caps[j]);
        double res = observed[n] - pred;
        double ar = fabs(res);
        loss += res*res;
        abs_sum += ar;
        if(ar > max_abs) max_abs = ar;
      }
      printf("%.6f,%.6f,%.12f,%.12f,%.12f,Calibration fit does not prove model validity validation and sensitivity review remain required.\n", rates[i], caps[j], loss, abs_sum/7.0, max_abs);
    }
  }
  return EXIT_SUCCESS;
}
