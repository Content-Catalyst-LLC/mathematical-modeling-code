package main

import "fmt"

type GovernanceRiskCase struct {
	Key               string
	ModelName         string
	ErrorRisk         float64
	UncertaintyLevel  float64
	ConsequenceLevel  float64
	ScopeMisuseRisk   float64
	AccountabilityGap float64
}

func governanceRiskScore(c GovernanceRiskCase) float64 {
	return 0.20*c.ErrorRisk +
		0.20*c.UncertaintyLevel +
		0.25*c.ConsequenceLevel +
		0.20*c.ScopeMisuseRisk +
		0.15*c.AccountabilityGap
}

func reviewClass(score float64) string {
	if score >= 0.70 {
		return "escalation_required"
	}
	if score >= 0.55 {
		return "governance_review_required"
	}
	return "standard_monitoring"
}

func main() {
	cases := []GovernanceRiskCase{
		{"infrastructure_risk", "Infrastructure risk prioritization model", 0.38, 0.56, 0.82, 0.42, 0.24},
		{"public_health_demand", "Public health demand model", 0.50, 0.68, 0.86, 0.48, 0.32},
		{"supply_chain_resilience", "Supply chain resilience model", 0.36, 0.52, 0.65, 0.40, 0.22},
		{"ai_triage_support", "AI-assisted triage support model", 0.62, 0.72, 0.95, 0.70, 0.55},
	}

	fmt.Println("key,error_risk,uncertainty_level,consequence_level,scope_misuse_risk,accountability_gap,governance_risk_score,review_class")
	for _, c := range cases {
		score := governanceRiskScore(c)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
			c.Key, c.ErrorRisk, c.UncertaintyLevel, c.ConsequenceLevel,
			c.ScopeMisuseRisk, c.AccountabilityGap, score, reviewClass(score))
	}
}
