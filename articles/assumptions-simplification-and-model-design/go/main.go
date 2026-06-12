package main

import "fmt"

type Scenario struct {
	Name         string
	InitialStock float64
	Capacity     float64
	Inflow       float64
	Demand       float64
	LossRate     float64
	Periods      int
}

func boundedUpdate(stock, inflow, demand, losses, capacity float64) float64 {
	next := stock + inflow - demand - losses
	if next < 0 {
		return 0
	}
	if next > capacity {
		return capacity
	}
	return next
}

func simulate(s Scenario) (finalStock float64, totalShortage float64) {
	stock := s.InitialStock
	for period := 0; period <= s.Periods; period++ {
		losses := s.LossRate * stock
		shortage := s.Demand + losses - (stock + s.Inflow)
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage
		stock = boundedUpdate(stock, s.Inflow, s.Demand, losses, s.Capacity)
	}
	return stock, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_baseline", 80, 100, 8, 6, 0.015, 60},
		{"go_compound_stress", 70, 80, 5, 7, 0.030, 60},
	}

	for _, scenario := range scenarios {
		final, shortage := simulate(scenario)
		fmt.Printf("%s final_stock=%.3f total_shortage=%.3f\n", scenario.Name, final, shortage)
	}
}
