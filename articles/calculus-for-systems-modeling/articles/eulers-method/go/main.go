package main

import (
	"fmt"
	"math"
)

func exactSolution(t float64, y0 float64, k float64) float64 {
	return y0 * math.Exp(-k*t)
}

func main() {
	y0 := 100.0
	k := 0.35
	h := 0.1
	stopTime := 20.0
	steps := int(math.Round(stopTime / h))
	y := y0
	multiplier := 1.0 - h*k
	status := "stable_for_simple_decay"
	if math.Abs(multiplier) > 1.0 {
		status = "unstable_risk"
	}

	fmt.Println("step,time,euler_value,exact_value,absolute_error,step_size,stability_multiplier,stability_status,warning")
	for step := 0; step <= steps; step++ {
		t := float64(step) * h
		exact := exactSolution(t, y0, k)
		fmt.Printf("%d,%.6f,%.12f,%.12f,%.12f,%.6f,%.12f,%s,Euler estimates depend on time step rate function initial condition stability and accumulated error.\n",
			step, t, y, exact, math.Abs(y-exact), h, multiplier, status)
		y = y + h*(-k*y)
	}
}
