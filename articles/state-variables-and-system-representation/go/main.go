package main

import "fmt"

type Scenario struct {
	Name             string
	Representation   string
	InitialStorage   float64
	InitialDemand    float64
	InitialCondition float64
	Capacity         float64
	Inflow           float64
	LossRate         float64
	DemandResponse   float64
	ConditionDecay   float64
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

func simulate(s Scenario) (finalStorage float64, finalDemand float64, finalCondition float64, totalShortage float64) {
	storage := s.InitialStorage
	demand := s.InitialDemand
	condition := s.InitialCondition

	for period := 0; period <= s.Periods; period++ {
		effectiveLossRate := s.LossRate
		if s.Representation == "condition_aware" {
			effectiveLossRate = s.LossRate * (1.0 + (1.0 - condition))
		}

		losses := effectiveLossRate * storage
		rawNext := storage + s.Inflow - demand - losses
		shortage := -rawNext
		if shortage < 0 {
			shortage = 0
		}
		totalShortage += shortage

		if s.Representation == "adaptive_demand" || s.Representation == "condition_aware" {
			demand -= s.DemandResponse * shortage
			if demand < 0 {
				demand = 0
			}
		}

		if s.Representation == "condition_aware" {
			condition -= s.ConditionDecay * shortage
			if condition < 0 {
				condition = 0
			}
		}

		storage = boundedUpdate(rawNext, s.Capacity)
	}

	return storage, demand, condition, totalShortage
}

func main() {
	scenarios := []Scenario{
		{"go_storage_only", "storage_only", 80, 7, 1.0, 100, 6, 0.015, 0.0, 0.0, 60},
		{"go_condition_aware", "condition_aware", 45, 8, 0.85, 80, 4, 0.020, 0.20, 0.002, 60},
	}

	for _, scenario := range scenarios {
		storage, demand, condition, shortage := simulate(scenario)
		fmt.Printf("%s representation=%s final_storage=%.3f final_demand=%.3f final_condition=%.3f total_shortage=%.3f\n",
			scenario.Name, scenario.Representation, storage, demand, condition, shortage)
	}
}
