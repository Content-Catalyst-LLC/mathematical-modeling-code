package main

import (
	"fmt"
	"math"
)

func mean(values []float64) float64 {
	total := 0.0
	for _, value := range values {
		total += value
	}
	return total / float64(len(values))
}

func sampleVariance(values []float64) float64 {
	m := mean(values)
	total := 0.0

	for _, value := range values {
		total += math.Pow(value-m, 2)
	}

	return total / float64(len(values)-1)
}

func main() {
	values := []float64{18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2}

	m := mean(values)
	variance := sampleVariance(values)
	sd := math.Sqrt(variance)

	fmt.Printf("Mean: %.6f\n", m)
	fmt.Printf("Sample variance: %.6f\n", variance)
	fmt.Printf("Sample standard deviation: %.6f\n", sd)
}
