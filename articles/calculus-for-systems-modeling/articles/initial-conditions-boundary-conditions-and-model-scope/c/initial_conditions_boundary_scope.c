#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("record_type,name,value_or_type,interpretation,warning\n");
  printf("initial_condition,population_stock,10 state units,synthetic teaching baseline,starting values need source and uncertainty notes\n");
  printf("boundary_condition,left_edge,no_flux,material does not leave through the left boundary,no-flux boundaries may overstate retention\n");
  printf("boundary_condition,right_edge,absorbing,material can leave the modeled domain,absorbing boundaries may understate feedback\n");
  printf("scope_record,temporal_scope,0 to 20 time units,short-horizon teaching simulation,do not interpret as long-term forecast\n");
  printf("scope_record,parameter_scope,growth_rate between 0.1 and 0.6,local sensitivity and teaching examples,do not use outside tested range without review\n");
  return EXIT_SUCCESS;
}
