package main

import "fmt"

type ModelCandidate struct {
	Key                   string
	ModelName             string
	ValidationScore       float64
	CalibrationError      float64
	SubgroupErrorGap      float64
	DriftScore            float64
	InterpretabilityScore float64
	PrivacyRisk           float64
	DeploymentCriticality float64
}

func governanceScore(c ModelCandidate) float64 {
	penalty := 1.8*c.CalibrationError +
		1.5*c.SubgroupErrorGap +
		1.2*c.DriftScore +
		1.4*c.PrivacyRisk +
		0.7*c.DeploymentCriticality -
		0.5*c.InterpretabilityScore
	return c.ValidationScore - penalty
}

func requiresReview(c ModelCandidate) bool {
	return c.CalibrationError > 0.08 ||
		c.SubgroupErrorGap > 0.12 ||
		c.DriftScore > 0.20 ||
		c.PrivacyRisk > 0.15 ||
		c.InterpretabilityScore < 0.50
}

func main() {
	candidates := []ModelCandidate{
		{"baseline_logistic", "Baseline logistic model", 0.76, 0.050, 0.080, 0.120, 0.920, 0.080, 0.62},
		{"tree_ensemble", "Tree ensemble", 0.83, 0.070, 0.140, 0.180, 0.620, 0.130, 0.70},
		{"neural_model", "Neural model", 0.86, 0.095, 0.190, 0.240, 0.380, 0.180, 0.82},
		{"constrained_model", "Constrained calibrated model", 0.81, 0.035, 0.060, 0.100, 0.780, 0.090, 0.66},
	}

	fmt.Println("key,validation_score,calibration_error,subgroup_error_gap,drift_score,privacy_risk,governance_score,requires_review")
	for _, candidate := range candidates {
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%t\n",
			candidate.Key,
			candidate.ValidationScore,
			candidate.CalibrationError,
			candidate.SubgroupErrorGap,
			candidate.DriftScore,
			candidate.PrivacyRisk,
			governanceScore(candidate),
			requiresReview(candidate))
	}
}
