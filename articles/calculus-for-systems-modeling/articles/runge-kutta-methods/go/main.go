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

func eulerStep(t float64, y float64, h float64, k float64) float64 {
	return y + h*rateFunction(t, y, k)
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
	eulerY := y0
	rkY := y0

	fmt.Println("step,time,euler_value,rk4_value,exact_value,euler_absolute_error,rk4_absolute_error,step_size,warning")
	for step := 0; step <= steps; step++ {
		t := float64(step) * h
		exact := exactSolution(t, y0, k)
		fmt.Printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.6f,Runge-Kutta estimates depend on rate function step size smoothness stiffness and benchmark comparison.\n",
			step, t, eulerY, rkY, exact, math.Abs(eulerY-exact), math.Abs(rkY-exact), h)
		eulerY = eulerStep(t, eulerY, h, k)
		rkY = rk4Step(t, rkY, h, k)
	}
}
