package main

import (
	"fmt"
	"math"
)

func exponentialPopulation(n0, r, t float64) float64 {
	return n0 * math.Exp(r*t)
}

func logisticPopulation(n0, r, k, t float64) float64 {
	return k / (1.0 + ((k-n0)/n0)*math.Exp(-r*t))
}

func main() {
	n0 := 100.0
	r := 0.08
	k := 1000.0
	fmt.Println("time,exponential,logistic")
	for t := 0; t <= 40; t++ {
		tf := float64(t)
		fmt.Printf("%d,%.6f,%.6f\n", t, exponentialPopulation(n0, r, tf), logisticPopulation(n0, r, k, tf))
	}
}
