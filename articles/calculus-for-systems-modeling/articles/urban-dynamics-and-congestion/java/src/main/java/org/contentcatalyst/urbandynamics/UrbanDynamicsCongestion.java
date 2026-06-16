package org.contentcatalyst.urbandynamics;
public class UrbanDynamicsCongestion {
  public static double trafficFlow(double density, double freeFlowSpeed, double jamDensity) { return Math.max(0.0, freeFlowSpeed * density * (1.0 - density / jamDensity)); }
  public static double bprTravelTime(double freeFlowTime, double volume, double capacity) { return freeFlowTime * (1.0 + 0.15 * Math.pow(volume / capacity, 4.0)); }
  public static double queueStep(double queue, double arrival, double service, double dt) { return Math.max(0.0, queue + (arrival - service) * dt); }
  public static void main(String[] args) {
    System.out.println("scenario_name,model_type,flow,travel_time,queue_step,warning");
    System.out.printf("below_capacity_corridor,link_flow,%.6f,%.6f,%.6f,flow_unit_and_boundary_must_be_documented%n", trafficFlow(35.0,60.0,140.0), bprTravelTime(20.0,1800.0,2000.0), queueStep(0.0,1800.0,2000.0,0.01));
    System.out.printf("over_capacity_bottleneck,queue_and_bpr,%.6f,%.6f,%.6f,over_capacity_delays_can_spill_back_upstream%n", trafficFlow(70.0,60.0,140.0), bprTravelTime(20.0,2300.0,2000.0), queueStep(0.0,2300.0,2000.0,0.01));
  }
}
