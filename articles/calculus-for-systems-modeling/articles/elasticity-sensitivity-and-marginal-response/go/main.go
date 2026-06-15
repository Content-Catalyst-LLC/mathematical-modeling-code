package main

import (
	"fmt"
	"math"
)

func responseFunction(x float64) float64 { return 10.0 * math.Sqrt(x+1.0) }
func analyticDerivative(x float64) float64 { return 5.0 / math.Sqrt(x+1.0) }
func elasticity(x float64) string {
	y := responseFunction(x)
	if x == 0.0 || y == 0.0 {
		return "NA"
	}
	return fmt.Sprintf("%.12f", (x/y)*analyticDerivative(x))
}

func main() {
	fmt.Println("x,value,derivative,elasticity")
	for _, x := range []float64{0.0, 0.5, 1.0, 4.0, 9.0, 24.0} {
		fmt.Printf("%.6f,%.12f,%.12f,%s\n", x, responseFunction(x), analyticDerivative(x), elasticity(x))
	}
}
