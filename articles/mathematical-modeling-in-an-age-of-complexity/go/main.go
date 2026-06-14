package main

import "fmt"

type ComplexityScenario struct {
	Key                  string
	ScenarioName         string
	StressLevel          float64
	InterdependenceLevel float64
	UncertaintyLevel     float64
	ResilienceScore      float64
	EquityScore          float64
	AdaptabilityScore    float64
}

func fragilityScore(s ComplexityScenario) float64 {
	return 0.35*s.StressLevel +
		0.30*s.InterdependenceLevel +
		0.25*s.UncertaintyLevel +
		0.10*(1.0-s.AdaptabilityScore)
}

func robustValue(s ComplexityScenario) float64 {
	f := fragilityScore(s)
	return 0.40*s.ResilienceScore +
		0.30*s.EquityScore +
		0.30*s.AdaptabilityScore -
		0.20*f
}

func main() {
	scenarios := []ComplexityScenario{
		{"baseline", "Baseline stress", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65},
		{"compound_shock", "Compound shock", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55},
		{"cascading_failure", "Cascading failure", 0.88, 0.86, 0.75, 0.32, 0.40, 0.42},
		{"adaptive_pathway", "Adaptive pathway", 0.65, 0.68, 0.70, 0.66, 0.70, 0.82},
	}

	fmt.Println("key,stress_level,interdependence_level,uncertainty_level,resilience_score,equity_score,adaptability_score,fragility_score,robust_value")
	for _, scenario := range scenarios {
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n",
			scenario.Key,
			scenario.StressLevel,
			scenario.InterdependenceLevel,
			scenario.UncertaintyLevel,
			scenario.ResilienceScore,
			scenario.EquityScore,
			scenario.AdaptabilityScore,
			fragilityScore(scenario),
			robustValue(scenario))
	}
}
