package main

import (
	"fmt"
	"math"
)

func linearModel(x float64) float64 {
	return 10.0 + 2.0*x
}

func exponentialModel(x float64) float64 {
	return 10.0 * math.Exp(0.18*x)
}

func logisticModel(x float64) float64 {
	return 100.0 / (1.0 + math.Exp(-0.75*(x-5.0)))
}

func thresholdModel(x float64) float64 {
	if x < 5.0 {
		return 20.0
	}
	return 80.0
}

func main() {
	x := 10.0
	fmt.Println("model,final_value")
	fmt.Printf("linear_growth,%.6f\n", linearModel(x))
	fmt.Printf("exponential_growth,%.6f\n", exponentialModel(x))
	fmt.Printf("logistic_growth,%.6f\n", logisticModel(x))
	fmt.Printf("threshold_response,%.6f\n", thresholdModel(x))
}
