package org.contentcatalyst.carbonpathways;

public class CarbonAccumulationPathways {
  public static double linearDecline(double e0, int year, int years) {
    return Math.max(0.0, e0 * (1.0 - ((double) year / (double) years)));
  }

  public static void main(String[] args) {
    double e0 = 40.0;
    int years = 30;
    double cumulative = 0.0;
    for (int y = 0; y <= years; y++) cumulative += linearDecline(e0, y, years);
    System.out.println("scenario_name,pathway_type,cumulative_emissions,warning");
    System.out.printf("linear_decline_to_zero,linear_decline,%.6f,linear_decline_still_accumulates_until_net_zero%n", cumulative);
  }
}
