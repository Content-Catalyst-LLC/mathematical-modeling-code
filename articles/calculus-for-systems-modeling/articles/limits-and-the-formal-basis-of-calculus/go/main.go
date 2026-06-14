package main

import (
	"fmt"
	"math"
)

func f(x float64) float64 {
	return math.Exp(0.2 * x)
}

func exactDerivative(x float64) float64 {
	return 0.2 * math.Exp(0.2*x)
}

func forwardDifference(x float64, h float64) float64 {
	return (f(x+h) - f(x)) / h
}

func centralDifference(x float64, h float64) float64 {
	return (f(x+h) - f(x-h)) / (2.0 * h)
}

func richardson(centralH float64, centralH2 float64) float64 {
	return (4.0*centralH2 - centralH) / 3.0
}

func main() {
	x := 5.0
	exact := exactDerivative(x)
	hValues := []float64{1.0, 0.5, 0.25, 0.125, 0.0625, 0.03125}

	fmt.Println("method,x,h,estimate,exact,absolute_error")

	for _, h := range hValues {
		fd := forwardDifference(x, h)
		cd := centralDifference(x, h)
		cd2 := centralDifference(x, h/2.0)
		rich := richardson(cd, cd2)

		fmt.Printf("forward_difference,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, fd, exact, math.Abs(fd-exact))
		fmt.Printf("central_difference,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, cd, exact, math.Abs(cd-exact))
		fmt.Printf("richardson_central,%.6f,%.6f,%.12f,%.12f,%.12f\n", x, h, rich, exact, math.Abs(rich-exact))
	}
}
