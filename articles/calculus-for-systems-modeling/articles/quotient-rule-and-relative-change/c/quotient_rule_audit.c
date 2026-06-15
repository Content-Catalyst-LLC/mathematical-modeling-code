#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double resource(double t){ return 1000.0 * exp(-0.01 * t); }
double resource_rate(double t){ return -0.01 * resource(t); }
double population(double t){ return 100.0 * exp(0.02 * t); }
double population_rate(double t){ return 0.02 * population(t); }

int main(void){
  double ts[]={0.0,5.0,10.0,20.0,40.0};
  printf("t,numerator,denominator,ratio,numerator_rate,denominator_rate,numerator_effect,denominator_effect,quotient_derivative,ratio_relative_rate\n");
  for(int i=0;i<5;i++){
    double t=ts[i], f=resource(t), g=population(t), fp=resource_rate(t), gp=population_rate(t);
    double ratio=f/g, ne=fp/g, de=-(f*gp)/(g*g), qd=ne+de;
    printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f\n",t,f,g,ratio,fp,gp,ne,de,qd,qd/ratio);
  }
  return EXIT_SUCCESS;
}
