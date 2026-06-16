package org.contentcatalyst.economicgrowth;

public class EconomicGrowthAdjustment {
  public static double exponentialOutput(double y0, double g, double t) {
    return y0 * Math.exp(g * t);
  }

  public static void main(String[] args) {
    double[] rates = {0.01, 0.025, 0.04};
    System.out.println("scenario_name,model_type,growth_rate,final_output,doubling_time,warning");
    for (double g : rates) {
      System.out.printf("growth_rate_case,exponential_growth,%.6f,%.6f,%.6f,growth_rate_assumptions_compound%n", g, exponentialOutput(100.0, g, 40.0), Math.log(2.0) / g);
    }
  }
}
