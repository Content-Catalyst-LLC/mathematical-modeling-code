package main

import "fmt"

func simulateLogistic(initialState, rate, capacity, dt float64, steps int) []float64 {
	state := make([]float64, steps)
	state[0] = initialState

	for i := 1; i < steps; i++ {
		derivative := rate * state[i-1] * (1.0 - state[i-1]/capacity)
		state[i] = state[i-1] + derivative*dt
	}

	return state
}

func main() {
	state := simulateLogistic(10.0, 0.20, 100.0, 0.1, 300)
	fmt.Printf("Final state: %.6f\n", state[len(state)-1])
}
