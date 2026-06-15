package main

import (
	"fmt"
	"math"
)

func resource(t float64) float64 { return 1000.0 * math.Exp(-0.01*t) }
func resourceRate(t float64) float64 { return -0.01 * resource(t) }
func population(t float64) float64 { return 100.0 * math.Exp(0.02*t) }
func populationRate(t float64) float64 { return 0.02 * population(t) }

func main() {
	fmt.Println("t,numerator,denominator,ratio,numerator_rate,denominator_rate,numerator_effect,denominator_effect,quotient_derivative,ratio_relative_rate")
	for _, t := range []float64{0.0, 5.0, 10.0, 20.0, 40.0} {
		f, g := resource(t), population(t)
		fp, gp := resourceRate(t), populationRate(t)
		ratio := f / g
		ne := fp / g
		de := -(f * gp) / (g * g)
		qd := ne + de
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f\n", t, f, g, ratio, fp, gp, ne, de, qd, qd/ratio)
	}
}
