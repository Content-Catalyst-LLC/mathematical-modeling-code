#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double equilibrium_state(double p){ return (-p + sqrt(p*p + 40.0)) / 2.0; }
double constraint(double x, double p){ return x*x + p*x - 10.0; }
double partial_state(double x, double p){ return 2.0*x + p; }
double partial_parameter(double x, double p){ (void)p; return x; }
double implicit_sensitivity(double x, double p){ return -partial_parameter(x,p) / partial_state(x,p); }

int main(void){
  double ps[]={-3.0,-1.0,0.0,1.0,3.0};
  printf("parameter,equilibrium_state,constraint_value,partial_state,partial_parameter,implicit_sensitivity\n");
  for(int i=0;i<5;i++){
    double p=ps[i], x=equilibrium_state(p), gx=partial_state(x,p), gp=partial_parameter(x,p), sens=implicit_sensitivity(x,p);
    printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n",p,x,constraint(x,p),gx,gp,sens);
  }
  return EXIT_SUCCESS;
}
