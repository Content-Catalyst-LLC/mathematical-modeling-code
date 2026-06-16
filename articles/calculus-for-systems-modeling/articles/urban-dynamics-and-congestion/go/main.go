package main
import ("fmt"; "math")
func trafficFlow(density, freeFlowSpeed, jamDensity float64) float64 { q := freeFlowSpeed*density*(1.0-density/jamDensity); if q < 0 { return 0 }; return q }
func bprTravelTime(freeFlowTime, volume, capacity float64) float64 { return freeFlowTime * (1.0 + 0.15*math.Pow(volume/capacity, 4.0)) }
func queueStep(queue, arrival, service, dt float64) float64 { q := queue + (arrival-service)*dt; if q < 0 { return 0 }; return q }
func main() {
	fmt.Println("scenario_name,model_type,flow,travel_time,queue_step,warning")
	fmt.Printf("below_capacity_corridor,link_flow,%.6f,%.6f,%.6f,flow_unit_and_boundary_must_be_documented\n", trafficFlow(35.0,60.0,140.0), bprTravelTime(20.0,1800.0,2000.0), queueStep(0.0,1800.0,2000.0,0.01))
	fmt.Printf("over_capacity_bottleneck,queue_and_bpr,%.6f,%.6f,%.6f,over_capacity_delays_can_spill_back_upstream\n", trafficFlow(70.0,60.0,140.0), bprTravelTime(20.0,2300.0,2000.0), queueStep(0.0,2300.0,2000.0,0.01))
}
