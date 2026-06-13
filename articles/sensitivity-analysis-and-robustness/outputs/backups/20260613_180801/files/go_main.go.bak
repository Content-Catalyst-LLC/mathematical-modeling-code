package main

import (
	"fmt"
	"math"
)

type Parameter struct {
	Name     string
	Baseline float64
	Low      float64
	High     float64
	Label    string
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

func main() {
	params := []Parameter{
		{"initial_stock", 80.0, 72.0, 88.0, "measurement"},
		{"growth_rate", 0.08, 0.04, 0.12, "parameter"},
		{"carrying_capacity", 120.0, 100.0, 140.0, "structural"},
		{"extraction_rate", 0.12, 0.08, 0.18, "policy"},
		{"shock_intensity", 0.03, 0.00, 0.08, "scenario"},
	}

	base := map[string]float64{}
	for _, p := range params {
		base[p.Name] = p.Baseline
	}

	baseOutput := projection(base["initial_stock"], base["growth_rate"], base["carrying_capacity"], base["extraction_rate"], base["shock_intensity"])
	fmt.Printf("baseline_output=%.6f\n", baseOutput)

	for _, p := range params {
		low := map[string]float64{}
		high := map[string]float64{}
		for k, v := range base {
			low[k] = v
			high[k] = v
		}
		low[p.Name] = p.Low
		high[p.Name] = p.High

		lowOutput := projection(low["initial_stock"], low["growth_rate"], low["carrying_capacity"], low["extraction_rate"], low["shock_intensity"])
		highOutput := projection(high["initial_stock"], high["growth_rate"], high["carrying_capacity"], high["extraction_rate"], high["shock_intensity"])
		fmt.Printf("%s range_width=%.6f\n", p.Name, math.Abs(highOutput-lowOutput))
	}
}
