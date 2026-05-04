package main

import "fmt"

func simulateLogistic(initialState float64, growthRate float64, carryingCapacity float64, timeSteps int) []float64 {
	state := make([]float64, timeSteps)
	state[0] = initialState

	for t := 1; t < timeSteps; t++ {
		state[t] = state[t-1] + growthRate*state[t-1]*(1.0-state[t-1]/carryingCapacity)
	}

	return state
}

func main() {
	state := simulateLogistic(10.0, 0.18, 100.0, 80)

	fmt.Println("Final state:")
	fmt.Printf("%.3f\n", state[len(state)-1])
}
