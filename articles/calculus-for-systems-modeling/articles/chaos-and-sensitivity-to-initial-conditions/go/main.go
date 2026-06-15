package main

import (
	"fmt"
	"math"
)

func logisticMap(x, r float64) float64 {
	return r * x * (1 - x)
}

func main() {
	r := 3.9
	xReference := 0.2
	xPerturbed := 0.2 + 1e-8
	fmt.Println("step,x_reference,x_perturbed,absolute_difference,log_difference,warning")
	for step := 0; step <= 100; step++ {
		difference := math.Abs(xReference - xPerturbed)
		logDifference := 0.0
		if difference > 0 {
			logDifference = math.Log(difference)
		}
		fmt.Printf("%d,%.12f,%.12f,%.12e,%.12f,Trajectory divergence depends on parameter value initial uncertainty numerical precision and iteration count.\n", step, xReference, xPerturbed, difference, logDifference)
		xReference = logisticMap(xReference, r)
		xPerturbed = logisticMap(xPerturbed, r)
	}
}
