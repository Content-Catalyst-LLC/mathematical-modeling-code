package main

import (
	"fmt"
	"math"
)

func tailFunction(x float64) float64 { return math.Exp(-0.4 * x) }

func trap(fn func(float64) float64, a float64, b float64, n int) float64 {
	dx := (b - a) / float64(n)
	total := 0.0
	for i := 0; i < n; i++ {
		x0 := a + dx*float64(i)
		x1 := x0 + dx
		total += 0.5 * (fn(x0) + fn(x1)) * dx
	}
	return total
}

func main() {
	cutoffs := []float64{2, 4, 8, 12, 20}
	reference := 1.0 / 0.4
	fmt.Println("cutoff,truncated_value,reference_value,tail_error")
	for _, cutoff := range cutoffs {
		truncated := trap(tailFunction, 0.0, cutoff, 4000)
		tailError := reference - truncated
		fmt.Printf("%.6f,%.12f,%.12f,%.12f\n", cutoff, truncated, reference, tailError)
	}
}
