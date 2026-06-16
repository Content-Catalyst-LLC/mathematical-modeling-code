#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("record_type,name,value,unit,interpretation,warning\n");
  printf("unit_record,population_stock,40,state units,synthetic teaching value,synthetic value do not treat as empirical measurement\n");
  printf("unit_record,carrying_capacity,100,state units,synthetic teaching capacity,capacity scale controls normalized interpretation\n");
  printf("unit_record,growth_rate,0.35,per time unit,synthetic teaching rate,rate units must match the time variable\n");
  printf("scale_record,stock_scale,100,state units,carrying capacity used to normalize population stock,changing the scale changes dimensionless stock\n");
  printf("nondimensional_record,scaled_stock,0.4,dimensionless,population stock as fraction of carrying capacity,dimensionless form depends on documented scale\n");
  return EXIT_SUCCESS;
}
