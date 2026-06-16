package main

import (
	"fmt"
	"math"
)

func exponentialOutput(y0, g, t float64) float64 {
	return y0 * math.Exp(g*t)
}

func main() {
	rates := []float64{0.01, 0.025, 0.04}
	fmt.Println("scenario_name,model_type,growth_rate,final_output,doubling_time,warning")
	for _, g := range rates {
		fmt.Printf("growth_rate_case,exponential_growth,%.6f,%.6f,%.6f,growth_rate_assumptions_compound\n", g, exponentialOutput(100.0, g, 40.0), math.Log(2.0)/g)
	}
}
