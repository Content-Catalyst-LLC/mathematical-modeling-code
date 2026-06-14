package main

import "fmt"

type Scenario struct {
	Name         string
	InitialState float64
	Rate         float64
	Capacity     float64
	Dt           float64
	Steps        int
}

func simulate(s Scenario) float64 {
	state := s.InitialState
	for i := 0; i < s.Steps; i++ {
		derivative := s.Rate * state * (1.0 - state/s.Capacity)
		state = state + derivative*s.Dt
		if state < 0 {
			state = 0
		}
	}
	return state
}

func main() {
	scenarios := []Scenario{
		{"baseline", 10.0, 0.20, 100.0, 0.1, 300},
		{"slow_adjustment", 10.0, 0.10, 100.0, 0.1, 300},
		{"high_capacity", 10.0, 0.20, 140.0, 0.1, 300},
	}

	fmt.Println("scenario,final_state")
	for _, scenario := range scenarios {
		fmt.Printf("%s,%.6f\n", scenario.Name, simulate(scenario))
	}
}
