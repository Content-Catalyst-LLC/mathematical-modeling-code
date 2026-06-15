package main

import (
	"fmt"
	"math"
)

func logistic(x float64) float64 { return 1.0 / (1.0 + math.Exp(-x)) }
func firstDerivative(x float64) float64 {
	y := logistic(x)
	return y * (1.0 - y)
}
func secondDerivative(x float64) float64 {
	y := logistic(x)
	return y * (1.0 - y) * (1.0 - 2.0*y)
}
func curvature(x float64) float64 {
	fp := firstDerivative(x)
	fpp := secondDerivative(x)
	return math.Abs(fpp) / math.Pow(1.0+fp*fp, 1.5)
}

func main() {
	fmt.Println("x,value,first_derivative,second_derivative,curvature")
	for _, x := range []float64{-4.0, -2.0, -1.0, 0.0, 1.0, 2.0, 4.0} {
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f\n", x, logistic(x), firstDerivative(x), secondDerivative(x), curvature(x))
	}
}
