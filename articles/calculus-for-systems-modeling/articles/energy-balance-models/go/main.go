package main
import "fmt"
func equilibriumTemperature(forcing, feedback float64) float64 { return forcing / feedback }
func adjustmentTime(heatCapacity, feedback float64) float64 { return heatCapacity / feedback }
func absorbedSolar(solarConstant, albedo float64) float64 { return solarConstant * (1.0 - albedo) / 4.0 }
func main() {
	fmt.Println("scenario_name,model_type,equilibrium_temperature,adjustment_time,absorbed_solar,warning")
	fmt.Printf("baseline_one_layer,one_layer,%.6f,%.6f,%.6f,boundaries_and_feedback_must_be_documented\n", equilibriumTemperature(3.7, 1.2), adjustmentTime(10.0, 1.2), absorbedSolar(1361.0, 0.30))
	fmt.Printf("stronger_feedback,one_layer,%.6f,%.6f,%.6f,feedback_strength_changes_response\n", equilibriumTemperature(3.7, 1.8), adjustmentTime(10.0, 1.8), absorbedSolar(1361.0, 0.30))
}
