package main

import "fmt"

type Scenario struct {
	Name             string
	InitialStorage   float64
	Capacity         float64
	InflowPerDay     float64
	DemandPerDay     float64
	LossRatePerDay   float64
	DeltaTDays       float64
	Periods          int
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

func simulate(s Scenario) (finalStorage float64, minFraction float64, maxFraction float64, totalShortage float64) {
	storage := s.InitialStorage
	minFraction = 1.0
	maxFraction = 0.0

	for period := 0; period <= s.Periods; period++ {
		inflowVolume := s.DeltaTDays * s.InflowPerDay
		demandVolume := s.DeltaTDays * s.DemandPerDay
		lossVolume := s.DeltaTDays * s.LossRatePerDay * storage
		rawNext := storage + inflowVolume - demandVolume - lossVolume

		shortage := -rawNext
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage

		storage = boundedUpdate(rawNext, s.Capacity)
		fraction := storage / s.Capacity

		if fraction < minFraction {
			minFraction = fraction
		}
		if fraction > maxFraction {
			maxFraction = fraction
		}
	}

	return storage, minFraction, maxFraction, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_daily_baseline", 80, 100, 8, 6, 0.015, 1, 60},
		{"go_weekly_step", 80, 100, 8, 6, 0.015, 7, 12},
	}

	for _, scenario := range scenarios {
		final, minFrac, maxFrac, shortage := simulate(scenario)
		fmt.Printf("%s final_storage=%.3f min_fraction=%.3f max_fraction=%.3f total_shortage=%.3f\n",
			scenario.Name, final, minFrac, maxFrac, shortage)
	}
}
