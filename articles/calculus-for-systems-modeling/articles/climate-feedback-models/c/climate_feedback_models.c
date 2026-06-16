#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double one_box(double forcing, double feedback, double heat_capacity, double time){
  double equilibrium = forcing / feedback;
  return equilibrium * (1.0 - exp(-(feedback / heat_capacity) * time));
}

int main(void){
  double forcing=3.7, c=8.0;
  printf("time,weak_feedback,baseline_feedback,strong_feedback\n");
  for(int t=0;t<=100;t+=10){
    printf("%d,%.6f,%.6f,%.6f\n", t, one_box(forcing,0.9,c,t), one_box(forcing,1.2,c,t), one_box(forcing,1.6,c,t));
  }
  return EXIT_SUCCESS;
}
