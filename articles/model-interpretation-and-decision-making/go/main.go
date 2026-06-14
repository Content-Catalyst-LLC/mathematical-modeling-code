package main

import "fmt"

type DecisionOption struct {
	Key                string
	Name               string
	ExpectedStock      float64
	LowerBound         float64
	UpperBound         float64
	Burden             float64
	ConsequenceIfWrong float64
}

func decisionScore(option DecisionOption) float64 {
	penalty := 0.0
	if option.LowerBound < 45.0 {
		penalty = 8.0
	}
	return option.ExpectedStock - 0.8*option.Burden - 1.2*option.ConsequenceIfWrong - penalty
}

func main() {
	options := []DecisionOption{
		{"no_action", "No immediate action", 52.0, 38.0, 66.0, 1.0, 9.0},
		{"monitoring", "Formal monitoring", 54.0, 42.0, 68.0, 3.0, 6.0},
		{"moderate_intervention", "Moderate intervention", 60.0, 50.0, 72.0, 5.0, 4.0},
		{"strong_intervention", "Strong intervention", 68.0, 58.0, 78.0, 8.0, 2.0},
	}

	fmt.Println("key,option_name,decision_score,threshold_margin,robustness_class")
	for _, option := range options {
		class := "fragile"
		if option.LowerBound >= 45.0 {
			class = "robust"
		}
		fmt.Printf("%s,%s,%.3f,%.3f,%s\n", option.Key, option.Name, decisionScore(option), option.ExpectedStock-45.0, class)
	}
}
