package org.contentcatalyst.energybalance;
public class EnergyBalanceModels {
  public static double equilibriumTemperature(double forcing, double feedback) { return forcing / feedback; }
  public static double adjustmentTime(double heatCapacity, double feedback) { return heatCapacity / feedback; }
  public static double absorbedSolar(double solarConstant, double albedo) { return solarConstant * (1.0 - albedo) / 4.0; }
  public static void main(String[] args) {
    System.out.println("scenario_name,model_type,equilibrium_temperature,adjustment_time,absorbed_solar,warning");
    System.out.printf("baseline_one_layer,one_layer,%.6f,%.6f,%.6f,boundaries_and_feedback_must_be_documented%n", equilibriumTemperature(3.7, 1.2), adjustmentTime(10.0, 1.2), absorbedSolar(1361.0, 0.30));
    System.out.printf("stronger_feedback,one_layer,%.6f,%.6f,%.6f,feedback_strength_changes_response%n", equilibriumTemperature(3.7, 1.8), adjustmentTime(10.0, 1.8), absorbedSolar(1361.0, 0.30));
  }
}
