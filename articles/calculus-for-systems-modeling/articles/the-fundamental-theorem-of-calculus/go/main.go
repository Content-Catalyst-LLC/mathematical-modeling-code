package main

import (
	"fmt"
	"math"
)

func stateValue(t float64) float64 { return 50.0 + 2.0*t + 3.0*math.Sin(t) }
func rateValue(t float64) float64 { return 2.0 + 3.0*math.Cos(t) }

func main() {
	times := []float64{0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2}
	accumulatedRate := 0.0

	for i := 0; i < len(times)-1; i++ {
		dt := times[i+1] - times[i]
		accumulatedRate += 0.5 * (rateValue(times[i]) + rateValue(times[i+1])) * dt
	}

	endpointDifference := stateValue(times[len(times)-1]) - stateValue(times[0])
	residual := endpointDifference - accumulatedRate

	fmt.Println("interval_start,interval_end,endpoint_difference,accumulated_rate,residual")
	fmt.Printf("%.6f,%.6f,%.12f,%.12f,%.12f\n", times[0], times[len(times)-1], endpointDifference, accumulatedRate, residual)
}
