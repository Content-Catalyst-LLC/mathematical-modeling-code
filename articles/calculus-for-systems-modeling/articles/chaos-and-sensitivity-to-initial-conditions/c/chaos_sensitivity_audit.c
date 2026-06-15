#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double logistic_map(double x, double r){ return r*x*(1.0-x); }

int main(void){
  double r = 3.9;
  double x_reference = 0.2;
  double x_perturbed = 0.2 + 1e-8;
  printf("step,x_reference,x_perturbed,absolute_difference,log_difference,warning\n");
  for(int step=0; step<=100; step++){
    double difference = fabs(x_reference - x_perturbed);
    double log_difference = difference > 0.0 ? log(difference) : 0.0;
    printf("%d,%.12f,%.12f,%.12g,%.12f,Trajectory divergence depends on parameter value initial uncertainty numerical precision and iteration count.\n", step, x_reference, x_perturbed, difference, log_difference);
    x_reference = logistic_map(x_reference, r);
    x_perturbed = logistic_map(x_perturbed, r);
  }
  return EXIT_SUCCESS;
}
