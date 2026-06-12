package main

import (
	"fmt"
	"math"
)

type Observation struct {
	Stock      float64
	Extraction float64
}

func observations() []Observation {
	return []Observation{
		{70.0, 5.5},
		{72.8, 5.8},
		{74.1, 6.2},
		{75.0, 6.4},
		{75.5, 6.8},
		{75.2, 7.0},
		{74.7, 7.1},
		{73.8, 7.4},
		{72.6, 7.6},
		{71.2, 7.8},
	}
}

func score(growthRate float64, carryingCapacity float64, data []Observation) float64 {
	stock := data[0].Stock
	sse := 0.0
	for i, obs := range data {
		predicted := stock
		if i > 0 {
			previous := data[i-1]
			growth := growthRate * stock * (1.0 - stock/carryingCapacity)
			predicted = math.Max(0.0, stock+growth-previous.Extraction)
			stock = predicted
		}
		residual := obs.Stock - predicted
		sse += residual * residual
	}
	return sse
}

func main() {
	data := observations()
	bestSSE := math.Inf(1)
	bestG := 0.0
	bestK := 0.0

	for g := 0.08; g <= 0.2600001; g += 0.01 {
		for k := 85.0; k <= 125.0001; k += 5.0 {
			sse := score(g, k, data)
			if sse < bestSSE {
				bestSSE = sse
				bestG = g
				bestK = k
			}
		}
	}

	fmt.Printf("best_growth_rate=%.4f best_carrying_capacity=%.4f sse=%.6f\n", bestG, bestK, bestSSE)
}
