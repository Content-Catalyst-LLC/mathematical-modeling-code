package org.contentcatalyst.coupledsystems;

public class CoupledHumanNaturalSystems {
  public static double regeneration(double stock, double growthRate, double carryingCapacity) {
    return growthRate * stock * (1.0 - stock / carryingCapacity);
  }

  public static double extraction(double efficiency, double effort, double stock) {
    return efficiency * effort * stock;
  }

  public static double naturalStockStep(double stock, double growthRate, double carryingCapacity, double harvest, double stress, double dt) {
    return Math.max(0.0, stock + (regeneration(stock, growthRate, carryingCapacity) - harvest - stress) * dt);
  }

  public static void main(String[] args) {
    double stock = 80.0;
    double harvest = extraction(0.003, 12.0, stock);
    double next = naturalStockStep(stock, 0.08, 100.0, harvest, 0.25, 0.25);
    System.out.println("scenario_name,regeneration,extraction,next_stock,warning");
    System.out.printf("baseline_coupled_resource,%.6f,%.6f,%.6f,boundary_human_natural_and_governance_assumptions_required%n", regeneration(stock, 0.08, 100.0), harvest, next);
  }
}
