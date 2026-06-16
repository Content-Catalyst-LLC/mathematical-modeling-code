package org.contentcatalyst.population;
public class PopulationDynamics {
  public static double exponential(double n0, double r, double t) { return n0 * Math.exp(r * t); }
  public static double logistic(double n0, double r, double k, double t) { return k / (1.0 + ((k - n0) / n0) * Math.exp(-r * t)); }
  public static void main(String[] args) {
    double n0 = 100.0, r = 0.08, k = 1000.0;
    System.out.println("time,exponential,logistic");
    for (int t = 0; t <= 40; t += 5) System.out.printf("%d,%.6f,%.6f%n", t, exponential(n0, r, t), logistic(n0, r, k, t));
  }
}
