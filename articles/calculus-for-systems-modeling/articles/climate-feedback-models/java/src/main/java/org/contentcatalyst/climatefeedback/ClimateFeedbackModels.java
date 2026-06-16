package org.contentcatalyst.climatefeedback;

public class ClimateFeedbackModels {
  public static double oneBox(double forcing, double feedback, double heatCapacity, double time) {
    double equilibrium = forcing / feedback;
    return equilibrium * (1.0 - Math.exp(-(feedback / heatCapacity) * time));
  }

  public static void main(String[] args) {
    double forcing = 3.7;
    double c = 8.0;
    System.out.println("time,weak_feedback,baseline_feedback,strong_feedback");
    for (int t = 0; t <= 100; t += 10) {
      System.out.printf("%d,%.6f,%.6f,%.6f%n", t, oneBox(forcing, 0.9, c, t), oneBox(forcing, 1.2, c, t), oneBox(forcing, 1.6, c, t));
    }
  }
}
