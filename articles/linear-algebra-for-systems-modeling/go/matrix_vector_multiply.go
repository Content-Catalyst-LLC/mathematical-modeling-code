package main

import "fmt"

func main() {
	A := [3][3]float64{
		{0.82, 0.10, 0.08},
		{0.12, 0.76, 0.12},
		{0.06, 0.18, 0.76},
	}

	x := [3]float64{0.70, 0.20, 0.10}
	y := [3]float64{0.0, 0.0, 0.0}

	for i := 0; i < 3; i++ {
		for j := 0; j < 3; j++ {
			y[i] += A[i][j] * x[j]
		}
	}

	fmt.Printf("Transformed state: %.6f %.6f %.6f\n", y[0], y[1], y[2])
}
