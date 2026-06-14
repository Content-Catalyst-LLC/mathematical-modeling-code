package main

import (
	"fmt"
	"math"
)

func systemResponse(x float64) float64 {
	return math.Exp(0.2 * x)
}

func exactDerivative(x float64) float64 {
	return 0.2 * math.Exp(0.2*x)
}

func differenceQuotient(x float64, h float64) float64 {
	return (systemResponse(x+h) - systemResponse(x)) / h
}

func main() {
	x := 5.0
	exact := exactDerivative(x)
	hValues := []float64{1.0, 0.5, 0.1, 0.05, 0.01, 0.005, 0.001}

	fmt.Println("function_name,x,h,estimate,exact_value,absolute_error")
	for _, h := range hValues {
		estimate := differenceQuotient(x, h)
		fmt.Printf("exp(0.2x),%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, estimate, exact, math.Abs(estimate-exact))
	}
}
