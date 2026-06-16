package org.contentcatalyst.predatorprey;

public class PredatorPreySystems {
  public static void main(String[] args) {
    double alpha = 0.6, beta = 0.02, gamma = 0.5, delta = 0.01;
    double x = 40.0, y = 9.0, dt = 0.02;
    for (int i = 0; i < 4000; i++) {
      double dx = alpha * x - beta * x * y;
      double dy = delta * x * y - gamma * y;
      x = Math.max(0.0, x + dt * dx);
      y = Math.max(0.0, y + dt * dy);
    }
    System.out.println("scenario_name,model_type,final_prey,final_predator,warning");
    System.out.printf("classic_lotka_volterra,lotka_volterra,%.6f,%.6f,mass_action_baseline%n", x, y);
  }
}
