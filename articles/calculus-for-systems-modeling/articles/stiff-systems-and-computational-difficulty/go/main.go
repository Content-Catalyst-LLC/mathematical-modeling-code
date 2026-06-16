package main

import (
	"fmt"
	"math"
)

func exactSolution(t, y0, lambda float64) float64 { return y0 * math.Exp(lambda*t) }
func explicitValue(y0, lambda, h, stopTime float64) float64 {
	steps := int(math.Round(stopTime / h))
	amp := 1 + h*lambda
	y := y0
	for i := 0; i < steps; i++ { y *= amp }
	return y
}
func implicitValue(y0, lambda, h, stopTime float64) float64 {
	steps := int(math.Round(stopTime / h))
	amp := 1 / (1 - h*lambda)
	y := y0
	for i := 0; i < steps; i++ { y *= amp }
	return y
}
func status(amp float64) string {
	if amp <= 1 { return "stable_for_test_problem" }
	return "unstable_for_test_problem"
}
func main() {
	y0 := 1.0
	lambda := -50.0
	stopTime := 1.0
	exactFinal := exactSolution(stopTime, y0, lambda)
	fmt.Println("step_size,eigenvalue,method,amplification_factor,stability_status,final_value,exact_final_value,absolute_error,warning")
	for _, h := range []float64{0.1, 0.05, 0.025, 0.01} {
		ev := explicitValue(y0, lambda, h, stopTime)
		eamp := math.Abs(1 + h*lambda)
		iv := implicitValue(y0, lambda, h, stopTime)
		iamp := math.Abs(1 / (1 - h*lambda))
		fmt.Printf("%.6f,%.6f,explicit_euler,%.12f,%s,%.12f,%.12f,%.12f,Explicit methods may require very small steps on stiff systems.\n", h, lambda, eamp, status(eamp), ev, exactFinal, math.Abs(ev-exactFinal))
		fmt.Printf("%.6f,%.6f,implicit_euler,%.12f,%s,%.12f,%.12f,%.12f,Implicit stability does not remove accuracy review.\n", h, lambda, iamp, status(iamp), iv, exactFinal, math.Abs(iv-exactFinal))
	}
}
