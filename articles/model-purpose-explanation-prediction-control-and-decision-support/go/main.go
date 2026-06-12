package main

import "fmt"

type Scenario struct {
	Name          string
	Purpose       string
	InitialStock  float64
	Capacity      float64
	Inflow        float64
	Demand        float64
	LossRate      float64
	ControlAction float64
	Periods       int
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
		effectiveDemand := s.Demand - s.ControlAction
		if effectiveDemand < 0 {
			effectiveDemand = 0
		}
		losses := s.LossRate * stock
		shortage := effectiveDemand + losses - (stock + s.Inflow)
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage
		stock = boundedUpdate(stock, s.Inflow, effectiveDemand, losses, s.Capacity)
	}
	return stock, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_explanation", "explanation", 80, 100, 8, 6, 0.015, 0, 60},
		{"go_prediction", "prediction", 80, 100, 5, 6, 0.015, 0, 60},
		{"go_control", "control", 80, 100, 5, 6, 0.015, 1.5, 60},
		{"go_decision_support", "decision_support", 70, 80, 5, 7, 0.030, 0.5, 60},
	}

	for _, scenario := range scenarios {
		final, shortage := simulate(scenario)
		fmt.Printf("%s purpose=%s final_stock=%.3f total_shortage=%.3f\n", scenario.Name, scenario.Purpose, final, shortage)
	}
}
