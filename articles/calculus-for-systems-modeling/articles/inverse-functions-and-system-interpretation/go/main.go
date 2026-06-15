package main

import (
	"fmt"
	"math"
)

func forwardModel(x float64) float64 { return math.Log1p(x) }
func forwardDerivative(x float64) float64 { return 1.0 / (1.0 + x) }
func inverseModel(y float64) float64 { return math.Exp(y) - 1.0 }

func main() {
	fmt.Println("target_output,recovered_input,forward_check,residual,forward_derivative,inverse_sensitivity,domain_valid")
	for _, y := range []float64{0.0, 0.5, 1.0, 1.5, 2.0} {
		x := inverseModel(y)
		ycheck := forwardModel(x)
		residual := ycheck - y
		derivative := forwardDerivative(x)
		invsens := 1.0 / derivative
		domainValid := x > -1.0
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%t\n", y, x, ycheck, residual, derivative, invsens, domainValid)
	}
}
