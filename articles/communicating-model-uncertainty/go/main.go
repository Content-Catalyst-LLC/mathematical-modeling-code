package main

import "fmt"

type CommunicationRecord struct {
	Key       string
	Layer     string
	Audience  string
	Status    string
	Statement string
}

func priority(record CommunicationRecord) float64 {
	score := 5.0
	if record.Status == "active" {
		score = 1.0
	}
	if record.Layer == "decision_threshold" || record.Layer == "governance" || record.Layer == "model_limit" {
		score += 2.0
	}
	if record.Audience == "public" || record.Audience == "decision_maker" {
		score += 1.0
	}
	return score
}

func main() {
	records := []CommunicationRecord{
		{"central_result", "result", "decision_maker", "active", "The baseline result is conditional on current assumptions."},
		{"uncertainty_range", "uncertainty", "public", "review", "Outcomes cover a range rather than one exact number."},
		{"threshold_risk", "decision_threshold", "decision_maker", "review", "Some plausible runs cross the action threshold."},
		{"structural_limit", "model_limit", "technical_reviewer", "review", "The model does not fully represent regime change."},
		{"use_limit", "governance", "future_user", "review", "The model should not be used outside the validated domain."},
	}

	fmt.Println("key,communication_layer,audience,status,priority")
	for _, r := range records {
		fmt.Printf("%s,%s,%s,%s,%.2f\n", r.Key, r.Layer, r.Audience, r.Status, priority(r))
	}
}
