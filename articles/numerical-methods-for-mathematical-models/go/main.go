package main

import "fmt"

func derivative(stock float64, growthRate float64, carryingCapacity float64, extraction float64) float64 {
	return growthRate*stock*(1.0-stock/carryingCapacity) - extraction
}

func runEuler(stepSize float64) float64 {
	stock := 70.0
	growthRate := 0.18
	carryingCapacity := 100.0
	extraction := 6.0
	horizon := 50.0
	steps := int(horizon / stepSize)

	for i := 0; i < steps; i++ {
		stock = stock + stepSize*derivative(stock, growthRate, carryingCapacity, extraction)
		if stock < 0 {
			stock = 0
		}
	}
	return stock
}

func main() {
	stepSizes := []float64{1.0, 0.5, 0.25, 0.1}
	reference := runEuler(0.1)

	for _, h := range stepSizes {
		finalStock := runEuler(h)
		diff := finalStock - reference
		if diff < 0 {
			diff = -diff
		}
		fmt.Printf("h=%.3f final_stock=%.6f difference_from_finest=%.6f\n", h, finalStock, diff)
	}
}
