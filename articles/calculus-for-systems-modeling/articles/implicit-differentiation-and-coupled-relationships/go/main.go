package main

import (
	"fmt"
	"math"
)

func equilibriumState(p float64) float64 { return (-p + math.Sqrt(p*p+40.0)) / 2.0 }
func constraint(x, p float64) float64 { return x*x + p*x - 10.0 }
func partialState(x, p float64) float64 { return 2.0*x + p }
func partialParameter(x, p float64) float64 { return x }

func main() {
	fmt.Println("parameter,equilibrium_state,constraint_value,partial_state,partial_parameter,implicit_sensitivity")
	for _, p := range []float64{-3.0, -1.0, 0.0, 1.0, 3.0} {
		x := equilibriumState(p)
		gx := partialState(x, p)
		gp := partialParameter(x, p)
		sens := -gp / gx
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n", p, x, constraint(x, p), gx, gp, sens)
	}
}
