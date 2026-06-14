package main

import "fmt"

type ModelRiskCase struct {
	Key               string
	ModelName         string
	IntendedUse       string
	Severity          float64
	Likelihood        float64
	DetectabilityGap  float64
	UncertaintyLevel  float64
	EquityConcern     float64
	AccountabilityGap float64
}

func ethicalRiskScore(c ModelRiskCase) float64 {
	return 1.8*c.Severity +
		1.3*c.Likelihood +
		1.2*c.DetectabilityGap +
		1.1*c.UncertaintyLevel +
		1.5*c.EquityConcern +
		1.6*c.AccountabilityGap
}

func reviewClass(score float64) string {
	if score >= 6.0 {
		return "high_ethics_review_required"
	}
	if score >= 4.0 {
		return "governance_review_required"
	}
	return "standard_review"
}

func main() {
	cases := []ModelRiskCase{
		{"exploratory_model", "Exploratory planning model", "learning and scenario discussion", 0.35, 0.35, 0.25, 0.60, 0.30, 0.25},
		{"allocation_model", "Resource allocation model", "prioritizing scarce resources", 0.85, 0.55, 0.55, 0.65, 0.75, 0.70},
		{"public_dashboard", "Public risk dashboard", "communicating population risk", 0.70, 0.50, 0.45, 0.80, 0.55, 0.60},
		{"automated_score", "Automated scoring model", "triggering institutional action", 0.90, 0.60, 0.70, 0.60, 0.80, 0.85},
	}

	fmt.Println("key,severity,likelihood,detectability_gap,uncertainty_level,equity_concern,accountability_gap,ethical_risk_score,review_class")
	for _, item := range cases {
		score := ethicalRiskScore(item)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
			item.Key,
			item.Severity,
			item.Likelihood,
			item.DetectabilityGap,
			item.UncertaintyLevel,
			item.EquityConcern,
			item.AccountabilityGap,
			score,
			reviewClass(score))
	}
}
