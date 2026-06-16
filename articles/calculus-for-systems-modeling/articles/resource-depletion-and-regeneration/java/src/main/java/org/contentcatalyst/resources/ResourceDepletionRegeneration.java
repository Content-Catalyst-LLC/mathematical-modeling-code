package org.contentcatalyst.resources;

public class ResourceDepletionRegeneration {
  public static double logisticRegeneration(double stock, double r, double k) {
    return Math.max(0.0, r * stock * (1.0 - stock / k));
  }

  public static void main(String[] args) {
    double stock = 600.0;
    double harvest = 35.0;
    double dt = 0.1;
    double cumulative = 0.0;
    for (int i = 0; i < 800; i++) {
      double extraction = Math.min(stock, harvest * dt);
      double growth = logisticRegeneration(stock, 0.18, 1000.0) * dt;
      stock = Math.max(0.0, stock + growth - extraction);
      cumulative += extraction;
    }
    System.out.println("scenario_name,resource_type,final_stock,cumulative_extraction,warning");
    System.out.printf("renewable_precautionary_harvest,renewable_logistic,%.6f,%.6f,precautionary_harvest%n", stock, cumulative);
  }
}
