package main

import "fmt"

type Direction struct {
	Key string
	Complexity, Maturity, Governance, Uncertainty, Judgment float64
}

func priority(d Direction) float64 {
	return 0.25*d.Complexity + 0.20*d.Maturity + 0.20*d.Governance + 0.20*d.Uncertainty + 0.15*d.Judgment
}

func reviewClass(d Direction) string {
	score := priority(d)
	if d.Governance >= 0.85 || d.Judgment >= 0.90 { return "governance_priority" }
	if d.Uncertainty >= 0.85 { return "uncertainty_priority" }
	if score >= 0.78 { return "strategic_priority" }
	return "monitor"
}

func main() {
	directions := []Direction{
		{"hybrid_models",0.88,0.70,0.74,0.72,0.80},
		{"ai_assistance",0.82,0.78,0.90,0.76,0.92},
		{"digital_twins",0.86,0.75,0.88,0.70,0.84},
		{"uncertainty_workflows",0.90,0.72,0.82,0.92,0.86},
		{"participatory_modeling",0.78,0.62,0.86,0.68,0.94},
	}
	fmt.Println("key,complexity_relevance,technical_maturity,governance_need,uncertainty_pressure,human_judgment_need,future_priority_score,review_class")
	for _, d := range directions {
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n", d.Key, d.Complexity, d.Maturity, d.Governance, d.Uncertainty, d.Judgment, priority(d), reviewClass(d))
	}
}
