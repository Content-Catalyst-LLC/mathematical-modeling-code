package main

import "fmt"

type Scenario struct {
	Name           string
	InitialStorage float64
	InitialDemand  float64
	Capacity       float64
	Inflow         float64
	LossRate       float64
	DemandResponse float64
	Periods        int
	AdaptiveDemand bool
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

func simulate(s Scenario) (finalStorage float64, finalDemand float64, totalShortage float64, totalOverflow float64) {
	storage := s.InitialStorage
	demand := s.InitialDemand

	for period := 0; period <= s.Periods; period++ {
		rawNext := storage + s.Inflow - demand - s.LossRate*storage
		shortage := -rawNext
		if shortage < 0 {
			shortage = 0
		}
		overflow := rawNext - s.Capacity
		if overflow < 0 {
			overflow = 0
		}

		totalShortage += shortage
		totalOverflow += overflow

		if s.AdaptiveDemand {
			demand -= s.DemandResponse * shortage
			if demand < 0 {
				demand = 0
			}
		}

		storage = boundedUpdate(rawNext, s.Capacity)
	}

	return storage, demand, totalShortage, totalOverflow
}

func main() {
	scenarios := []Scenario{
		{"go_baseline", 80, 7, 100, 6, 0.015, 0.0, 60, false},
		{"go_adaptive", 45, 10, 80, 4, 0.020, 0.20, 60, true},
	}

	for _, scenario := range scenarios {
		storage, demand, shortage, overflow := simulate(scenario)
		fmt.Printf("%s final_storage=%.3f final_demand=%.3f total_shortage=%.3f total_overflow=%.3f\n",
			scenario.Name, storage, demand, shortage, overflow)
	}
}
