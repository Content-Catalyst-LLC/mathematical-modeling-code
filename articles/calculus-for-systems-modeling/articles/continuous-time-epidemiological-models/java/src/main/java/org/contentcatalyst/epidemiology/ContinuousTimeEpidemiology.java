package org.contentcatalyst.epidemiology;

public class ContinuousTimeEpidemiology {
  public static double r0Value(double beta, double gamma) {
    return beta / gamma;
  }

  public static double doublingTime(double growth) {
    return growth <= 0 ? Double.POSITIVE_INFINITY : Math.log(2.0) / growth;
  }

  public static void main(String[] args) {
    System.out.println("scenario_name,model_type,reproduction_number,doubling_time,warning");
    System.out.printf("baseline_sir,SIR,%.6f,%.6f,baseline_model_assumptions%n", r0Value(0.32, 0.10), doublingTime(0.22));
    System.out.printf("reduced_transmission_sir,SIR,%.6f,%.6f,reduced_transmission_must_have_mechanism%n", r0Value(0.22, 0.10), doublingTime(0.12));
  }
}
