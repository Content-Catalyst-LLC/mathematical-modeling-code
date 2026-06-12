package main

import (
	"fmt"
	"math"
	"math/rand"
	"sort"
)

type Scenario struct {
	Name        string
	DemandMu    float64
	DemandSigma float64
	SupplyMean  float64
	SupplySD    float64
	Reserve     float64
	Simulations int
	Seed        int64
}

func quantile(values []float64, p float64) float64 {
	copied := append([]float64{}, values...)
	sort.Float64s(copied)
	idx := int(math.Round(p * float64(len(copied)-1)))
	if idx < 0 {
		idx = 0
	}
	if idx >= len(copied) {
		idx = len(copied) - 1
	}
	return copied[idx]
}

func simulate(s Scenario) (probability float64, expected float64, q95 float64, maxShortage float64) {
	rng := rand.New(rand.NewSource(s.Seed))
	shortages := make([]float64, 0, s.Simulations)
	events := 0

	for i := 0; i < s.Simulations; i++ {
		demand := math.Exp(s.DemandMu + s.DemandSigma*rng.NormFloat64())
		supply := s.SupplyMean + s.SupplySD*rng.NormFloat64()
		if supply < 0 {
			supply = 0
		}
		shortage := demand - (supply + s.Reserve)
		if shortage < 0 {
			shortage = 0
		}
		if shortage > 0 {
			events++
		}
		shortages = append(shortages, shortage)
		expected += shortage
		if shortage > maxShortage {
			maxShortage = shortage
		}
	}

	expected = expected / float64(s.Simulations)
	probability = float64(events) / float64(s.Simulations)
	q95 = quantile(shortages, 0.95)
	return
}

func main() {
	scenarios := []Scenario{
		{"go_baseline", 4.50, 0.25, 95, 8, 5, 5000, 101},
		{"go_high_variability", 4.50, 0.45, 95, 12, 5, 5000, 102},
	}

	for _, scenario := range scenarios {
		probability, expected, q95, maxShortage := simulate(scenario)
		fmt.Printf("%s shortage_probability=%.4f expected_shortage=%.4f q95=%.4f max_shortage=%.4f\n",
			scenario.Name, probability, expected, q95, maxShortage)
	}
}
