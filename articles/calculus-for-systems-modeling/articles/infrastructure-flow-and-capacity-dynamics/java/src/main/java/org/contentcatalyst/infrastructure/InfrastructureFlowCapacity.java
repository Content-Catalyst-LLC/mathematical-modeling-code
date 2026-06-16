package org.contentcatalyst.infrastructure;

public class InfrastructureFlowCapacity {
  public static double utilization(double arrival, double capacity) {
    return arrival / capacity;
  }

  public static double delayFunction(double u) {
    if (u >= 1.0) return 999.0;
    return 1.0 * (1.0 + 0.8 * (u / (1.0 - u)));
  }

  public static void main(String[] args) {
    double[] arrivals = {75.0, 95.0, 115.0};
    String[] names = {"baseline_spare_capacity", "near_capacity_operation", "over_capacity_backlog"};
    System.out.println("scenario_name,system_type,utilization,delay_warning");
    for (int i = 0; i < arrivals.length; i++) {
      double u = utilization(arrivals[i], 100.0);
      System.out.printf("%s,queue_capacity,%.6f,%.6f%n", names[i], u, delayFunction(Math.min(u, 0.999)));
    }
  }
}
