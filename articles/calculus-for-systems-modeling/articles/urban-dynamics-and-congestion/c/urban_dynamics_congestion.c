#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double traffic_flow(double density, double free_flow_speed, double jam_density){
  double q = free_flow_speed * density * (1.0 - density / jam_density);
  return q > 0.0 ? q : 0.0;
}
double bpr_travel_time(double free_flow_time, double volume, double capacity){
  return free_flow_time * (1.0 + 0.15 * pow(volume / capacity, 4.0));
}
double queue_step(double queue, double arrival, double service, double dt){
  double q = queue + (arrival - service) * dt;
  return q > 0.0 ? q : 0.0;
}
int main(void){
  printf("scenario_name,model_type,flow,travel_time,queue_step,warning\n");
  printf("below_capacity_corridor,link_flow,%.6f,%.6f,%.6f,flow_unit_and_boundary_must_be_documented\n", traffic_flow(35.0,60.0,140.0), bpr_travel_time(20.0,1800.0,2000.0), queue_step(0.0,1800.0,2000.0,0.01));
  printf("over_capacity_bottleneck,queue_and_bpr,%.6f,%.6f,%.6f,over_capacity_delays_can_spill_back_upstream\n", traffic_flow(70.0,60.0,140.0), bpr_travel_time(20.0,2300.0,2000.0), queue_step(0.0,2300.0,2000.0,0.01));
  return EXIT_SUCCESS;
}
