#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double population(double t){ return 100.0 * exp(0.01 * t); }
double population_rate(double t){ return 0.01 * population(t); }
double affluence(double t){ return 2.0 * exp(0.02 * t); }
double affluence_rate(double t){ return 0.02 * affluence(t); }

int main(void){
  double ts[]={0.0,5.0,10.0,20.0};
  printf("rule,model_structure,t,derivative_value,component_a,component_b,warning\n");
  for(int i=0;i<4;i++){
    double t=ts[i];
    double a=population_rate(t)*affluence(t);
    double b=population(t)*affluence_rate(t);
    printf("product_rule,impact = population * affluence,%.6f,%.12f,%.12f,%.12f,\n",t,a+b,a,b);
  }
  return EXIT_SUCCESS;
}
