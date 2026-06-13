package main

import (
	"fmt"
	"math"
)

func simulateModel(formKey string) float64 {
	stock := 80.0
	carryingCapacity := 120.0
	extractionRate := 0.12
	growthRate := 0.08
	fixedLoss := 5.8
	criticalThreshold := 55.0

	for year := 0; year < 10; year++ {
		switch formKey {
		case "linear_decline":
			stock = math.Max(0.0, stock-fixedLoss)
		case "proportional_decline":
			stock = math.Max(0.0, stock-extractionRate*stock)
		case "logistic_recovery":
			growth := growthRate * stock * (1.0 - stock/carryingCapacity)
			extraction := extractionRate * stock
			stock = math.Max(0.0, stock+growth-extraction)
		case "threshold_shift":
			if stock < criticalThreshold {
				stock = math.Max(0.0, stock-1.6*extractionRate*stock)
			} else {
				stock = math.Max(0.0, stock-extractionRate*stock)
			}
		}
	}
	return stock
}

func main() {
	forms := []string{"linear_decline", "proportional_decline", "logistic_recovery", "threshold_shift"}
	minValue := math.Inf(1)
	maxValue := math.Inf(-1)

	fmt.Println("model_form,projected_stock,below_threshold")
	for _, form := range forms {
		y := simulateModel(form)
		if y < minValue {
			minValue = y
		}
		if y > maxValue {
			maxValue = y
		}
		fmt.Printf("%s,%.6f,%t\n", form, y, y < 45.0)
	}

	fmt.Printf("structural_spread,%.6f\n", maxValue-minValue)
}
