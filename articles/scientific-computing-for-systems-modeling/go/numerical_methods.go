package main

import (
	"fmt"
	"math"
)

func trapezoidIntegral(start, end float64, intervals int) float64 {
	width := (end - start) / float64(intervals)
	total := 0.0

	for i := 1; i <= intervals; i++ {
		x0 := start + float64(i-1)*width
		x1 := start + float64(i)*width
		y0 := math.Sin(x0) + 1.5
		y1 := math.Sin(x1) + 1.5
		total += 0.5 * (y0 + y1) * width
	}

	return total
}

func main() {
	estimate := trapezoidIntegral(0.0, 10.0, 500)
	fmt.Printf("Trapezoid integral estimate: %.8f\n", estimate)
}
