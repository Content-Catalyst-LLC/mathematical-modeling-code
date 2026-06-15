package main

import (
	"fmt"
	"math"
)

func equilibrium(input, loss float64) float64 { return input / loss }
func rateLaw(y, input, loss float64) float64 { return input - loss*y }
func analytical(t, y0, input, loss float64) float64 {
	eq := equilibrium(input, loss)
	return eq + (y0-eq)*math.Exp(-loss*t)
}

func main() {
	y0 := 20.0
	y := 20.0
	input := 12.0
	loss := 0.4
	dt := 0.1
	eq := equilibrium(input, loss)
	fmt.Println("scenario,time,analytical_state,euler_state,absolute_error,input_rate,loss_rate,equilibrium,initial_state,method,warning")
	for n := 0; n <= 100; n++ {
		t := float64(n) * dt
		a := analytical(t, y0, input, loss)
		fmt.Printf("input_loss_balance,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,analytical_vs_explicit_euler,Assumes constant input and proportional loss.\n", t, a, y, math.Abs(a-y), input, loss, eq, y0)
		y += dt * rateLaw(y, input, loss)
	}
}
