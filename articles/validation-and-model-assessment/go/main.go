package main

import (
	"fmt"
	"math"
)

type Observation struct {
	Observed  float64
	Predicted float64
	Scenario  string
}

func observations() []Observation {
	return []Observation{
		{70.1, 70.8, "holdout"},
		{68.9, 69.7, "holdout"},
		{67.4, 68.3, "holdout"},
		{65.8, 66.9, "holdout"},
		{64.2, 65.1, "holdout"},
		{62.1, 63.8, "stress"},
		{60.4, 61.3, "stress"},
		{58.8, 59.9, "stress"},
	}
}

func main() {
	data := observations()
	sumAbs := 0.0
	sumSq := 0.0
	bias := 0.0
	maxAbs := 0.0

	for _, obs := range data {
		residual := obs.Observed - obs.Predicted
		absError := math.Abs(residual)
		sumAbs += absError
		sumSq += residual * residual
		bias += residual
		if absError > maxAbs {
			maxAbs = absError
		}
	}

	n := float64(len(data))
	rmse := math.Sqrt(sumSq / n)
	mae := sumAbs / n
	bias = bias / n

	fitness := "not_adequate_without_revision"
	if rmse <= 1.25 && maxAbs <= 2.0 {
		fitness = "adequate_for_scenario_screening"
	} else if rmse <= 2.5 {
		fitness = "limited_use_requires_review"
	}

	fmt.Printf("rmse=%.4f mae=%.4f bias=%.4f max_abs_error=%.4f fitness=%s\n", rmse, mae, bias, maxAbs, fitness)
}
