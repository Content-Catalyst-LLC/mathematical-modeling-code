#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double emissions(double t){ return 50.0 * exp(0.015 * t); }
double emissions_rate(double t){ return 0.015 * emissions(t); }
double concentration(double e){ return 0.5 * e; }
double d_concentration_d_emissions(double e){ (void)e; return 0.5; }
double forcing(double c){ return log(1.0 + c); }
double d_forcing_d_concentration(double c){ return 1.0 / (1.0 + c); }
double temperature_response(double f){ return 1.2 * f; }
double d_temperature_d_forcing(double f){ (void)f; return 1.2; }

int main(void){
  double ts[]={0.0,5.0,10.0,20.0,40.0};
  printf("t,emissions,concentration,forcing,temperature,emissions_rate,d_concentration_d_emissions,d_forcing_d_concentration,d_temperature_d_forcing,total_derivative\n");
  for(int i=0;i<5;i++){
    double t=ts[i], e=emissions(t), c=concentration(e), f=forcing(c), temp=temperature_response(f);
    double s1=emissions_rate(t), s2=d_concentration_d_emissions(e), s3=d_forcing_d_concentration(c), s4=d_temperature_d_forcing(f);
    printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f\n",t,e,c,f,temp,s1,s2,s3,s4,s4*s3*s2*s1);
  }
  return EXIT_SUCCESS;
}
