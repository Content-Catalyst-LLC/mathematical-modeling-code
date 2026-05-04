package main

import "fmt"

func logisticRate(state, growthRate, capacity float64) float64 {
	return growthRate * state * (1.0 - state/capacity)
}

func simulateLogistic(initialState, growthRate, capacity, dt float64, steps int) []float64 {
	state := make([]float64, steps)
	state[0] = initialState

	for i := 1; i < steps; i++ {
		derivative := logisticRate(state[i-1], growthRate, capacity)
		state[i] = state[i-1] + derivative*dt
	}

	return state
}

func main() {
	state := simulateLogistic(10.0, 0.20, 100.0, 0.1, 300)
	fmt.Printf("Final state: %.6f\n", state[len(state)-1])
}
