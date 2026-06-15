#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double volume(double h){ return 12.0*h*h; }
double d_volume_d_height(double h){ return 24.0*h; }
double height_path(double t){ return 2.0 + 0.08*t; }
double height_rate(double t){ (void)t; return 0.08; }

int main(void){
  double ts[]={0.0,5.0,10.0,20.0,40.0};
  printf("time,height,height_rate,volume,structural_derivative,inferred_volume_rate\n");
  for(int i=0;i<5;i++){
    double t=ts[i], h=height_path(t), hr=height_rate(t), v=volume(h), structural=d_volume_d_height(h), inferred=structural*hr;
    printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n",t,h,hr,v,structural,inferred);
  }
  return EXIT_SUCCESS;
}
