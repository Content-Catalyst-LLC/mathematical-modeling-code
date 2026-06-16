package main
import "fmt"

func regeneration(stock, growthRate, carryingCapacity float64) float64 {
	return growthRate * stock * (1.0 - stock/carryingCapacity)
}
func extraction(efficiency, effort, stock float64) float64 {
	return efficiency * effort * stock
}
func naturalStockStep(stock, growthRate, carryingCapacity, harvest, stress, dt float64) float64 {
	next := stock + (regeneration(stock, growthRate, carryingCapacity)-harvest-stress)*dt
	if next < 0 { return 0 }
	return next
}
func main() {
	stock := 80.0
	harvest := extraction(0.003, 12.0, stock)
	next := naturalStockStep(stock, 0.08, 100.0, harvest, 0.25, 0.25)
	fmt.Println("scenario_name,regeneration,extraction,next_stock,warning")
	fmt.Printf("baseline_coupled_resource,%.6f,%.6f,%.6f,boundary_human_natural_and_governance_assumptions_required\n", regeneration(stock, 0.08, 100.0), harvest, next)
}
