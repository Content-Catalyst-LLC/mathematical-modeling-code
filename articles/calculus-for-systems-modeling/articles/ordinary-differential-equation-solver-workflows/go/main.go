package main

import (
	"fmt"
	"math"
)

func rateFunction(t float64, y float64, k float64) float64 {
	_ = t
	return -k * y
}

func exactSolution(t float64, y0 float64, k float64) float64 {
	return y0 * math.Exp(-k*t)
}

func rk4Step(t float64, y float64, h float64, k float64) float64 {
	k1 := rateFunction(t, y, k)
	k2 := rateFunction(t+h/2, y+h*k1/2, k)
	k3 := rateFunction(t+h/2, y+h*k2/2, k)
	k4 := rateFunction(t+h, y+h*k3, k)
	return y + (h/6)*(k1+2*k2+2*k3+k4)
}

func main() {
	y0 := 100.0
	k := 0.35
	h := 0.5
	stopTime := 20.0
	steps := int(math.Round(stopTime / h))
	y := y0

	fmt.Println("step,time,solver_value,exact_value,absolute_error,solver_method,step_size,warning")
	for step := 0; step <= steps; step++ {
		t := float64(step) * h
		exact := exactSolution(t, y0, k)
		fmt.Printf("%d,%.6f,%.12f,%.12f,%.12f,fixed_step_rk4,%.6f,ODE solver outputs depend on equation initial condition method tolerances step size stiffness and diagnostics.\n",
			step, t, y, exact, math.Abs(y-exact), h)
		y = rk4Step(t, y, h, k)
	}
}
