package main

import "fmt"

type Scenario struct {
	Name             string
	InitialStorage   float64
	Capacity         float64
	BaseInflow       float64
	BaseDemand       float64
	DemandGrowth     float64
	LossRate         float64
	Periods          int
}

func boundedUpdate(storage, inflow, demand, losses, capacity float64) float64 {
	next := storage + inflow - demand - losses
	if next < 0 {
		return 0
	}
	if next > capacity {
		return capacity
	}
	return next
}

func simulate(s Scenario) (finalStorage float64, totalShortage float64) {
	storage := s.InitialStorage
	for period := 0; period <= s.Periods; period++ {
		demand := s.BaseDemand
		for i := 0; i < period; i++ {
			demand *= 1.0 + s.DemandGrowth
		}
		losses := s.LossRate * storage
		shortage := demand + losses - (storage + s.BaseInflow)
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage
		storage = boundedUpdate(storage, s.BaseInflow, demand, losses, s.Capacity)
	}
	return storage, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_baseline", 80, 100, 8, 6, 0.010, 0.015, 60},
		{"go_stress", 75, 100, 5, 6.5, 0.030, 0.030, 60},
	}

	for _, scenario := range scenarios {
		final, shortage := simulate(scenario)
		fmt.Printf("%s final_storage=%.3f total_shortage=%.3f\n", scenario.Name, final, shortage)
	}
}
