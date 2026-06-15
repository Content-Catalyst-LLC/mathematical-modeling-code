package main

import (
	"fmt"
	"math"
)

func population(t float64) float64 { return 100.0 * math.Exp(0.01*t) }
func populationRate(t float64) float64 { return 0.01 * population(t) }
func affluence(t float64) float64 { return 2.0 * math.Exp(0.02*t) }
func affluenceRate(t float64) float64 { return 0.02 * affluence(t) }

func main() {
	fmt.Println("rule,model_structure,t,derivative_value,component_a,component_b,warning")
	for _, t := range []float64{0.0, 5.0, 10.0, 20.0} {
		a := populationRate(t) * affluence(t)
		b := population(t) * affluenceRate(t)
		fmt.Printf("product_rule,impact = population * affluence,%.6f,%.12f,%.12f,%.12f,\n", t, a+b, a, b)
	}
}
