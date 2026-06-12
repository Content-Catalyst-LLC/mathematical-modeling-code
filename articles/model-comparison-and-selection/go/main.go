package main

import (
	"fmt"
	"math"
)

type Candidate struct {
	ID                string
	Family            string
	CalibrationRMSE   float64
	ValidationRMSE    float64
	ParameterCount    int
	Interpretability  float64
	Robustness        float64
	DecisionRelevance float64
}

func score(m Candidate) float64 {
	return m.ValidationRMSE +
		0.08*float64(m.ParameterCount) -
		0.35*m.Interpretability -
		0.40*m.Robustness -
		0.35*m.DecisionRelevance
}

func main() {
	models := []Candidate{
		{"baseline_naive", "baseline", 2.90, 3.05, 0, 0.95, 0.72, 0.55},
		{"linear_trend", "statistical", 1.80, 2.10, 2, 0.88, 0.70, 0.68},
		{"logistic_growth", "mechanistic", 1.25, 1.42, 3, 0.76, 0.82, 0.86},
		{"stochastic_shock", "stochastic", 1.05, 1.60, 6, 0.58, 0.88, 0.90},
		{"high_flex_curve", "flexible", 0.45, 2.75, 9, 0.35, 0.40, 0.52},
	}

	bestScore := math.Inf(1)
	bestID := ""

	for _, model := range models {
		current := score(model)
		overfitGap := model.ValidationRMSE - model.CalibrationRMSE
		fmt.Printf("%s comparison_score=%.4f overfit_gap=%.4f\n", model.ID, current, overfitGap)
		if current < bestScore {
			bestScore = current
			bestID = model.ID
		}
	}

	fmt.Printf("selected_model=%s comparison_score=%.4f\n", bestID, bestScore)
}
