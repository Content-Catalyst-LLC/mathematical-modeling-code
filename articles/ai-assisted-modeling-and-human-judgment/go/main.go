package main

import "fmt"

type HumanJudgmentCase struct {
	Key                   string
	JudgmentPoint         string
	DecisionContext       string
	EvidenceStrength      float64
	UncertaintyLevel      float64
	ConsequenceLevel      float64
	AutomationBiasRisk    float64
	AccountabilityClarity float64
}

func judgmentRiskScore(c HumanJudgmentCase) float64 {
	return 0.25*(1.0-c.EvidenceStrength) +
		0.25*c.UncertaintyLevel +
		0.25*c.ConsequenceLevel +
		0.15*c.AutomationBiasRisk +
		0.10*(1.0-c.AccountabilityClarity)
}

func reviewClass(score float64) string {
	if score >= 0.65 {
		return "escalation_required"
	}
	if score >= 0.50 {
		return "human_review_required"
	}
	return "standard_review"
}

func main() {
	cases := []HumanJudgmentCase{
		{"problem_frame", "problem framing", "public infrastructure stress model", 0.72, 0.58, 0.80, 0.45, 0.70},
		{"data_fit", "data fitness judgment", "using administrative records", 0.62, 0.66, 0.75, 0.50, 0.65},
		{"model_use", "approved use decision", "moving from exploratory to decision support", 0.68, 0.70, 0.88, 0.72, 0.55},
		{"public_summary", "communication approval", "publishing model results", 0.76, 0.62, 0.82, 0.60, 0.72},
	}

	fmt.Println("key,evidence_strength,uncertainty_level,consequence_level,automation_bias_risk,accountability_clarity,judgment_risk_score,review_class")
	for _, item := range cases {
		score := judgmentRiskScore(item)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
			item.Key,
			item.EvidenceStrength,
			item.UncertaintyLevel,
			item.ConsequenceLevel,
			item.AutomationBiasRisk,
			item.AccountabilityClarity,
			score,
			reviewClass(score))
	}
}
