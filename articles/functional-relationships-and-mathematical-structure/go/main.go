package main

import "fmt"

type Scenario struct {
	Name             string
	Structure        string
	InitialStock     float64
	Capacity         float64
	Inflow           float64
	Demand           float64
	LossRate         float64
	FeedbackStrength float64
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

func simulate(s Scenario) (finalStock float64, totalShortage float64, totalOverflow float64) {
	stock := s.InitialStock
	demand := s.Demand

	for period := 0; period <= s.Periods; period++ {
		losses := s.LossRate * stock
		rawNext := stock + s.Inflow - demand - losses

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

		nextStock := rawNext
		if s.Structure == "constrained" || s.Structure == "feedback" {
			nextStock = boundedUpdate(rawNext, s.Capacity)
		}

		if s.Structure == "feedback" {
			demand = demand - s.FeedbackStrength*shortage
			if demand < 0 {
				demand = 0
			}
		}

		stock = nextStock
	}

	return stock, totalShortage, totalOverflow
}

func main() {
	scenarios := []Scenario{
		{"go_linear", "linear", 80, 100, 8, 6, 0.015, 0, 60},
		{"go_constrained", "constrained", 80, 100, 8, 6, 0.015, 0, 60},
		{"go_feedback", "feedback", 40, 60, 3, 7, 0.050, 0.20, 60},
	}

	for _, scenario := range scenarios {
		final, shortage, overflow := simulate(scenario)
		fmt.Printf("%s structure=%s final_stock=%.3f total_shortage=%.3f total_overflow=%.3f\n", scenario.Name, scenario.Structure, final, shortage, overflow)
	}
}
