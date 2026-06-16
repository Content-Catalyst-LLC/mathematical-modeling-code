package main

import (
	"fmt"
	"math"
)

func exactSolution(t, y0, k float64) float64 { return y0 * math.Exp(-k*t) }
func rateFunction(t, y, k float64) float64 { _ = t; return -k * y }
func rk4Step(t, y, h, k float64) float64 {
	k1 := rateFunction(t, y, k)
	k2 := rateFunction(t+h/2, y+h*k1/2, k)
	k3 := rateFunction(t+h/2, y+h*k2/2, k)
	k4 := rateFunction(t+h, y+h*k3, k)
	return y + (h/6)*(k1+2*k2+2*k3+k4)
}
func simulate(y0, k, h, stopTime float64) float64 {
	steps := int(math.Round(stopTime / h))
	y := y0
	for step := 0; step < steps; step++ {
		y = rk4Step(float64(step)*h, y, h, k)
	}
	return y
}
func main() {
	y0 := 100.0
	k := 0.35
	stopTime := 20.0
	exactFinal := exactSolution(stopTime, y0, k)
	fmt.Println("step_size,steps,solver_method,final_numeric_value,final_exact_value,final_absolute_error,warning")
	for _, h := range []float64{1.0, 0.5, 0.25, 0.125} {
		numeric := simulate(y0, k, h, stopTime)
		fmt.Printf("%.6f,%d,fixed_step_rk4,%.12f,%.12f,%.12f,Convergence evidence supports numerical reliability not empirical validity.\n",
			h, int(math.Round(stopTime/h)), numeric, exactFinal, math.Abs(numeric-exactFinal))
	}
}
