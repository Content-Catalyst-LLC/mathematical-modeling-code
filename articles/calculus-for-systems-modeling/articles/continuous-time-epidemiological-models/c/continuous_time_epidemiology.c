#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double r0_value(double beta, double gamma){
  return beta / gamma;
}
double doubling_time(double growth){
  return growth <= 0.0 ? INFINITY : log(2.0) / growth;
}

int main(void){
  printf("scenario_name,model_type,reproduction_number,doubling_time,warning\n");
  printf("baseline_sir,SIR,%.6f,%.6f,baseline_model_assumptions\n", r0_value(0.32,0.10), doubling_time(0.22));
  printf("reduced_transmission_sir,SIR,%.6f,%.6f,reduced_transmission_must_have_mechanism\n", r0_value(0.22,0.10), doubling_time(0.12));
  return EXIT_SUCCESS;
}
