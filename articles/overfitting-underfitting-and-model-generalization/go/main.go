package main

import (
	"fmt"
	"math"
)

type Candidate struct {
	ID                 string
	Family             string
	TrainingRMSE       float64
	ValidationRMSE     float64
	ParameterCount     int
	Complexity         float64
	Interpretability   float64
}

func classify(model Candidate) string {
	gap := model.ValidationRMSE - model.TrainingRMSE
	if model.TrainingRMSE >= 3.0 && model.ValidationRMSE >= 3.0 {
		return "likely_underfit"
	}
	if gap >= 1.0 && model.TrainingRMSE <= 1.0 {
		return "likely_overfit"
	}
	if model.ValidationRMSE <= 1.5 && gap <= 0.6 {
		return "generalizes_reasonably"
	}
	return "requires_review"
}

func score(model Candidate) float64 {
	return model.ValidationRMSE +
		0.20*model.Complexity +
		0.08*float64(model.ParameterCount) -
		0.20*model.Interpretability
}

func main() {
	models := []Candidate{
		{"constant_baseline", "baseline", 3.40, 3.55, 0, 0.05, 0.95},
		{"linear_trend", "statistical", 1.95, 2.10, 2, 0.25, 0.88},
		{"logistic_growth", "mechanistic", 1.20, 1.38, 3, 0.45, 0.78},
		{"regularized_curve", "regularized", 0.95, 1.44, 5, 0.62, 0.66},
		{"high_flex_curve", "flexible", 0.28, 2.85, 10, 0.95, 0.30},
	}

	bestScore := math.Inf(1)
	bestID := ""

	for _, model := range models {
		current := score(model)
		gap := model.ValidationRMSE - model.TrainingRMSE
		fmt.Printf("%s generalization_score=%.4f overfit_gap=%.4f classification=%s\n", model.ID, current, gap, classify(model))
		if current < bestScore {
			bestScore = current
			bestID = model.ID
		}
	}

	fmt.Printf("selected_for_review=%s generalization_score=%.4f\n", bestID, bestScore)
}
