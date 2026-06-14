package main

import "fmt"

type PolicyOption struct {
	Key                       string
	OptionName                string
	ProjectedBenefit          float64
	TotalCost                 float64
	ImplementationFeasibility float64
	EquityScore               float64
	UncertaintyWidth          float64
	PublicRisk                float64
}

func publicValueScore(option PolicyOption) float64 {
	budgetPenalty := 0.0
	if option.TotalCost > 40.0 {
		budgetPenalty = 14.0
	}
	return option.ProjectedBenefit +
		18.0*option.ImplementationFeasibility +
		24.0*option.EquityScore -
		option.TotalCost -
		0.22*option.UncertaintyWidth -
		30.0*option.PublicRisk -
		budgetPenalty
}

func main() {
	options := []PolicyOption{
		{"baseline", "Maintain current services", 42.0, 18.0, 0.86, 0.52, 18.0, 0.42},
		{"targeted_prevention", "Targeted prevention program", 68.0, 32.0, 0.74, 0.78, 22.0, 0.30},
		{"broad_expansion", "Broad service expansion", 81.0, 49.0, 0.58, 0.69, 28.0, 0.34},
		{"adaptive_pathway", "Adaptive pathway with monitoring triggers", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24},
	}

	fmt.Println("key,projected_benefit,total_cost,equity_score,public_risk,public_value_score,budget_violation")
	for _, option := range options {
		fmt.Printf("%s,%.3f,%.3f,%.3f,%.3f,%.6f,%t\n",
			option.Key,
			option.ProjectedBenefit,
			option.TotalCost,
			option.EquityScore,
			option.PublicRisk,
			publicValueScore(option),
			option.TotalCost > 40.0)
	}
}
