package main

import (
	"fmt"
	"math"
)

type Scenario struct { Name string; Initial, Rate, Capacity, TimeHorizon float64 }

func validateDomain(s Scenario) string {
	if s.Initial < 0 { return "initial_state must be nonnegative" }
	if s.Rate < 0 { return "rate must be nonnegative" }
	if s.Capacity <= 0 { return "capacity must be positive" }
	if s.TimeHorizon < 0 { return "time_horizon must be nonnegative" }
	if s.Initial > s.Capacity { return "initial_state exceeds capacity" }
	return ""
}

func boundedGrowth(s Scenario) float64 {
	return s.Capacity / (1.0 + ((s.Capacity-s.Initial)/s.Initial)*math.Exp(-s.Rate*s.TimeHorizon))
}

func main() {
	scenarios := []Scenario{
		{"baseline", 10.0, 0.20, 100.0, 20.0},
		{"near_capacity", 95.0, 0.20, 100.0, 20.0},
		{"invalid_negative_state", -5.0, 0.20, 100.0, 20.0},
		{"outside_capacity", 120.0, 0.20, 100.0, 20.0},
	}
	fmt.Println("scenario,status,value_or_issue")
	for _, s := range scenarios {
		if issue := validateDomain(s); issue != "" {
			fmt.Printf("%s,domain_review,%s\n", s.Name, issue)
		} else {
			fmt.Printf("%s,ok,%.6f\n", s.Name, boundedGrowth(s))
		}
	}
}
