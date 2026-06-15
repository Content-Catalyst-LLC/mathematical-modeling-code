package main

import (
	"fmt"
	"math"
)

func main() {
	initialState := 80.0
	target := 100.0
	adjustmentRate := 0.2
	delay := 5.0
	dt := 0.1
	steps := 300
	delaySteps := int(math.Round(delay / dt))
	states := []float64{initialState}

	fmt.Println("step,time,current_state,delayed_state,derivative_value,target,absolute_gap,warning")
	for step := 0; step <= steps; step++ {
		time := float64(step) * dt
		current := states[len(states)-1]
		delayedIndex := step - delaySteps
		delayed := initialState
		if delayedIndex >= 0 {
			delayed = states[delayedIndex]
		}
		derivative := adjustmentRate * (target - delayed)
		fmt.Printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Delayed adjustment depends on delay length history function time step and feedback strength.\n",
			step, time, current, delayed, derivative, target, math.Abs(current-target))
		states = append(states, current+dt*derivative)
	}
}
