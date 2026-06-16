#include <iostream>
double equilibrium_temperature(double forcing, double feedback){ return forcing / feedback; }
double adjustment_time(double heat_capacity, double feedback){ return heat_capacity / feedback; }
double absorbed_solar(double solar_constant, double albedo){ return solar_constant * (1.0 - albedo) / 4.0; }
int main(){
  std::cout << "scenario_name,model_type,equilibrium_temperature,adjustment_time,absorbed_solar,warning\n";
  std::cout << "baseline_one_layer,one_layer," << equilibrium_temperature(3.7,1.2) << "," << adjustment_time(10.0,1.2) << "," << absorbed_solar(1361.0,0.30) << ",boundaries_and_feedback_must_be_documented\n";
  std::cout << "stronger_feedback,one_layer," << equilibrium_temperature(3.7,1.8) << "," << adjustment_time(10.0,1.8) << "," << absorbed_solar(1361.0,0.30) << ",feedback_strength_changes_response\n";
}
