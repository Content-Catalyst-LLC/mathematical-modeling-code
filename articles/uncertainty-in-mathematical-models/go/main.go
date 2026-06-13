package main

import (
	"fmt"
	"math"
	"math/rand"
	"sort"
)

type Parameter struct {
	Name string
	Low  float64
	High float64
}

func projection(initialStock, growthRate, carryingCapacity, extractionRate, shockIntensity float64) float64 {
	stock := initialStock
	for year := 0; year < 10; year++ {
		growth := growthRate * stock * (1.0 - stock/carryingCapacity)
		extraction := extractionRate * stock
		shock := shockIntensity * stock
		stock = math.Max(0.0, stock+growth-extraction-shock)
	}
	return stock
}

func quantile(values []float64, p float64) float64 {
	sorted := append([]float64{}, values...)
	sort.Float64s(sorted)
	idx := int(p * float64(len(sorted)-1))
	return sorted[idx]
}

func main() {
	rng := rand.New(rand.NewSource(42))
	parameters := []Parameter{
		{"initial_stock", 72.0, 88.0},
		{"growth_rate", 0.04, 0.12},
		{"carrying_capacity", 100.0, 140.0},
		{"extraction_rate", 0.08, 0.18},
		{"shock_intensity", 0.00, 0.08},
	}

	outputs := make([]float64, 0, 1000)
	thresholdCount := 0

	for i := 0; i < 1000; i++ {
		values := map[string]float64{}
		for _, p := range parameters {
			values[p.Name] = rng.Float64()*(p.High-p.Low) + p.Low
		}
		y := projection(values["initial_stock"], values["growth_rate"], values["carrying_capacity"], values["extraction_rate"], values["shock_intensity"])
		outputs = append(outputs, y)
		if y < 45.0 {
			thresholdCount++
		}
	}

	sum := 0.0
	for _, y := range outputs {
		sum += y
	}

	fmt.Printf("mean=%.6f p05=%.6f p95=%.6f threshold_probability=%.6f\n",
		sum/float64(len(outputs)),
		quantile(outputs, 0.05),
		quantile(outputs, 0.95),
		float64(thresholdCount)/float64(len(outputs)))
}
