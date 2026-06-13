package main

import (
	"fmt"
	"math"
)

type Scenario struct {
	Key                  string
	Form                 string
	Scenario             string
	ExtractionMultiplier float64
	Shock                float64
}

func simulate(form string, extractionMultiplier float64, shock float64) float64 {
	stock := 80.0
	carryingCapacity := 120.0
	growthRate := 0.08
	extractionRate := 0.12 * extractionMultiplier
	fixedLoss := 5.8 * extractionMultiplier
	criticalThreshold := 55.0

	for year := 0; year < 10; year++ {
		switch form {
		case "linear_decline":
			stock = math.Max(0.0, stock-fixedLoss-shock*stock)
		case "logistic_recovery":
			growth := growthRate * stock * (1.0 - stock/carryingCapacity)
			extraction := extractionRate * stock
			stock = math.Max(0.0, stock+growth-extraction-shock*stock)
		case "threshold_shift":
			if stock < criticalThreshold {
				stock = math.Max(0.0, stock-1.6*extractionRate*stock-shock*stock)
			} else {
				stock = math.Max(0.0, stock-extractionRate*stock-shock*stock)
			}
		}
	}
	return stock
}

func main() {
	scenarios := []Scenario{
		{"linear_baseline", "linear_decline", "baseline", 1.0, 0.00},
		{"linear_stress", "linear_decline", "stress", 1.25, 0.05},
		{"dynamic_baseline", "logistic_recovery", "baseline", 1.0, 0.00},
		{"dynamic_stress", "logistic_recovery", "stress", 1.25, 0.05},
		{"threshold_baseline", "threshold_shift", "baseline", 1.0, 0.00},
		{"threshold_stress", "threshold_shift", "stress", 1.25, 0.05},
	}

	minValue := math.Inf(1)
	maxValue := math.Inf(-1)

	fmt.Println("key,model_form,scenario,projected_stock,below_threshold")
	for _, s := range scenarios {
		y := simulate(s.Form, s.ExtractionMultiplier, s.Shock)
		if y < minValue {
			minValue = y
		}
		if y > maxValue {
			maxValue = y
		}
		fmt.Printf("%s,%s,%s,%.6f,%t\n", s.Key, s.Form, s.Scenario, y, y < 45.0)
	}

	fmt.Printf("robustness_spread,%.6f\n", maxValue-minValue)
}
