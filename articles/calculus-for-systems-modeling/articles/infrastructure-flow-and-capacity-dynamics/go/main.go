package main

import (
	"fmt"
	"math"
)

func delayFunction(u float64) float64 {
	if u >= 1.0 {
		return 999.0
	}
	return 1.0 * (1.0 + 0.8*(u/(1.0-u)))
}

func main() {
	arrivals := []float64{75.0, 95.0, 115.0}
	names := []string{"baseline_spare_capacity", "near_capacity_operation", "over_capacity_backlog"}
	fmt.Println("scenario_name,system_type,utilization,delay_warning")
	for i, arrival := range arrivals {
		u := arrival / 100.0
		fmt.Printf("%s,queue_capacity,%.6f,%.6f\n", names[i], u, delayFunction(math.Min(u, 0.999)))
	}
}
