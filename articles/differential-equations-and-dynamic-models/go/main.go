package main

import "fmt"

type Scenario struct {
	Name           string
	InitialStorage float64
	Capacity       float64
	InflowRate     float64
	DemandRate     float64
	LossRate       float64
	Dt             float64
	Horizon        float64
}

func derivative(storage float64, s Scenario) float64 {
	return s.InflowRate - s.DemandRate - s.LossRate*storage
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

func simulate(s Scenario) (finalStorage float64, minStorage float64, maxStorage float64, totalShortage float64) {
	storage := s.InitialStorage
	minStorage = storage
	maxStorage = storage
	steps := int(s.Horizon / s.Dt)

	for step := 0; step <= steps; step++ {
		if storage < minStorage {
			minStorage = storage
		}
		if storage > maxStorage {
			maxStorage = storage
		}

		rate := derivative(storage, s)
		rawNext := storage + s.Dt*rate
		shortage := -rawNext
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage
		storage = boundedUpdate(rawNext, s.Capacity)
	}

	return storage, minStorage, maxStorage, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_baseline", 80, 100, 8, 6, 0.015, 0.25, 60},
		{"go_high_demand", 80, 100, 8, 10, 0.015, 0.25, 60},
	}

	for _, scenario := range scenarios {
		final, minStorage, maxStorage, shortage := simulate(scenario)
		fmt.Printf("%s final_storage=%.3f min_storage=%.3f max_storage=%.3f total_shortage=%.3f\n",
			scenario.Name, final, minStorage, maxStorage, shortage)
	}
}
