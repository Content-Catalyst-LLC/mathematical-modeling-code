package org.contentcatalyst.financialdynamics;

public class FinancialDynamicsCompounding {
  public static double continuousFutureValue(double v0, double r, double t) {
    return v0 * Math.exp(r * t);
  }

  public static double continuousPresentValue(double fv, double r, double t) {
    return fv * Math.exp(-r * t);
  }

  public static void main(String[] args) {
    System.out.println("scenario_name,model_type,final_value,present_value,warning");
    System.out.printf("continuous_compounding_case,future_value,%.6f,1000.000000,continuous_compounding%n", continuousFutureValue(1000.0, 0.05, 30.0));
    System.out.printf("discounted_future_value,present_value,5000.000000,%.6f,discounting%n", continuousPresentValue(5000.0, 0.05, 30.0));
  }
}
