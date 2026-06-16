package main

import (
	"fmt"
	"math"
)

func r0Value(beta, gamma float64) float64 {
	return beta / gamma
}

func doublingTime(growth float64) float64 {
	if growth <= 0 {
		return math.Inf(1)
	}
	return math.Log(2.0) / growth
}

func main() {
	fmt.Println("scenario_name,model_type,reproduction_number,doubling_time,warning")
	fmt.Printf("baseline_sir,SIR,%.6f,%.6f,baseline_model_assumptions\n", r0Value(0.32, 0.10), doublingTime(0.22))
	fmt.Printf("reduced_transmission_sir,SIR,%.6f,%.6f,reduced_transmission_must_have_mechanism\n", r0Value(0.22, 0.10), doublingTime(0.12))
}
