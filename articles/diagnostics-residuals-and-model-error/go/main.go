package main

import (
	"fmt"
	"math"
)

type Observation struct {
	Time      int
	Group     string
	Observed  float64
	Predicted float64
	Threshold float64
}

func main() {
	data := []Observation{
		{1, "baseline", 82.0, 81.5, 70.0},
		{2, "baseline", 79.5, 80.2, 70.0},
		{3, "baseline", 77.0, 78.4, 70.0},
		{4, "baseline", 74.3, 75.6, 70.0},
		{5, "threshold", 71.5, 72.8, 70.0},
		{6, "threshold", 69.2, 71.0, 70.0},
		{7, "threshold", 67.8, 69.8, 70.0},
		{8, "stress", 65.5, 68.0, 70.0},
		{9, "stress", 63.0, 66.4, 70.0},
		{10, "stress", 61.1, 65.2, 70.0},
	}

	sumAbs := 0.0
	sumSq := 0.0
	bias := 0.0
	maxAbs := 0.0
	disagreements := 0

	for _, item := range data {
		residual := item.Observed - item.Predicted
		absError := math.Abs(residual)
		sumAbs += absError
		sumSq += residual * residual
		bias += residual
		if absError > maxAbs {
			maxAbs = absError
		}
		if (item.Observed < item.Threshold) != (item.Predicted < item.Threshold) {
			disagreements++
		}
	}

	n := float64(len(data))
	fmt.Printf("mean_error=%.4f mae=%.4f rmse=%.4f max_abs_error=%.4f decision_disagreements=%d\n",
		bias/n, sumAbs/n, math.Sqrt(sumSq/n), maxAbs, disagreements)
}
