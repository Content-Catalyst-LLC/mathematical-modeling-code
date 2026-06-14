package main

import "fmt"

type ResourceScenario struct {
	Key              string
	ScenarioName     string
	InitialStock     float64
	GrowthRate       float64
	CarryingCapacity float64
	Extraction       float64
	ClimateStress    float64
	Years            int
	MinimumStock     float64
}

type Evaluation struct {
	FinalStock              float64
	MinimumObservedStock    float64
	MinimumResilienceMargin float64
	ThresholdBreach         bool
}

func evaluate(s ResourceScenario) Evaluation {
	stock := s.InitialStock
	effectiveGrowth := s.GrowthRate * (1.0 - s.ClimateStress)
	minStock := stock
	minMargin := stock - s.MinimumStock

	for year := 0; year < s.Years; year++ {
		regeneration := effectiveGrowth * stock * (1.0 - stock/s.CarryingCapacity)
		stock = stock + regeneration - s.Extraction
		if stock < 0.0 {
			stock = 0.0
		}
		if stock < minStock {
			minStock = stock
		}
		margin := stock - s.MinimumStock
		if margin < minMargin {
			minMargin = margin
		}
	}

	return Evaluation{stock, minStock, minMargin, minStock < s.MinimumStock}
}

func main() {
	scenarios := []ResourceScenario{
		{"baseline", "Baseline managed use", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0},
		{"high_extraction", "High extraction pressure", 420.0, 0.24, 800.0, 64.0, 0.04, 25, 250.0},
		{"climate_stress", "Climate stress with lower regeneration", 420.0, 0.24, 800.0, 42.0, 0.22, 25, 250.0},
		{"restoration_pathway", "Restoration and reduced extraction", 420.0, 0.28, 860.0, 24.0, 0.03, 25, 250.0},
		{"adaptive_management", "Adaptive use with monitoring trigger", 420.0, 0.25, 820.0, 32.0, 0.08, 25, 250.0},
	}

	fmt.Println("key,final_stock,minimum_observed_stock,minimum_resilience_margin,threshold_breach")
	for _, scenario := range scenarios {
		eval := evaluate(scenario)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%t\n",
			scenario.Key,
			eval.FinalStock,
			eval.MinimumObservedStock,
			eval.MinimumResilienceMargin,
			eval.ThresholdBreach)
	}
}
