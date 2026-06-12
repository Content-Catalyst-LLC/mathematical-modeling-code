package main

import "fmt"

type Scenario struct {
	Name             string
	InitialStock     float64
	GrowthRate       float64
	CarryingCapacity float64
	Extraction       float64
	Steps            int
}

func simulate(s Scenario) float64 {
	stock := s.InitialStock
	for step := 0; step < s.Steps; step++ {
		growth := s.GrowthRate * stock * (1.0 - stock/s.CarryingCapacity)
		stock = stock + growth - s.Extraction
		if stock < 0 {
			stock = 0
		}
	}
	return stock
}

func main() {
	scenarios := []Scenario{
		{"baseline", 70.0, 0.18, 100.0, 6.0, 50},
		{"stress", 70.0, 0.15, 100.0, 9.0, 50},
		{"recovery_policy", 70.0, 0.18, 100.0, 5.0, 50},
	}

	fmt.Println("scenario,final_stock")
	for _, s := range scenarios {
		fmt.Printf("%s,%.6f\n", s.Name, simulate(s))
	}
}
