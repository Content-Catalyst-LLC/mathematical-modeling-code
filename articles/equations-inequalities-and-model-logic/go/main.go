package main

import "fmt"

type Scenario struct {
	Name                string
	InitialStock        float64
	Capacity            float64
	Inflow              float64
	Demand              float64
	LossRate            float64
	LowStorageThreshold float64
	DemandReduction     float64
	Periods             int
}

func boundedUpdate(rawNext, capacity float64) float64 {
	if rawNext < 0 {
		return 0
	}
	if rawNext > capacity {
		return capacity
	}
	return rawNext
}

func simulate(s Scenario) (finalStock float64, totalShortage float64, logicActivations int) {
	stock := s.InitialStock
	demand := s.Demand

	for period := 0; period <= s.Periods; period++ {
		losses := s.LossRate * stock
		rawNext := stock + s.Inflow - demand - losses

		shortage := -rawNext
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage

		if stock < s.LowStorageThreshold {
			logicActivations++
			demand -= s.DemandReduction
			if demand < 0 {
				demand = 0
			}
		}

		stock = boundedUpdate(rawNext, s.Capacity)
	}

	return stock, totalShortage, logicActivations
}

func main() {
	scenarios := []Scenario{
		{"go_baseline_logic", 80, 100, 8, 6, 0.015, 35, 0.5, 60},
		{"go_constraint_stress", 40, 60, 3, 7, 0.050, 25, 1.0, 60},
	}

	for _, scenario := range scenarios {
		final, shortage, activations := simulate(scenario)
		fmt.Printf("%s final_stock=%.3f total_shortage=%.3f logic_activations=%d\n", scenario.Name, final, shortage, activations)
	}
}
