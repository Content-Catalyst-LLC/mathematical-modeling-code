package main

import (
	"fmt"
	"math"
)

func main() {
	a, b, c, d := 3.0, 1.0, 2.0, 4.0
	y1, y2 := 7.0, 8.0

	det := a*d - b*c
	fmt.Printf("det(A) = %.8f\n", det)

	if math.Abs(det) < 1e-12 {
		fmt.Println("Matrix is singular or numerically near-singular.")
		return
	}

	x1 := (d*y1 - b*y2) / det
	x2 := (-c*y1 + a*y2) / det

	r1 := a*x1 + b*x2 - y1
	r2 := c*x1 + d*x2 - y2
	residualNorm := math.Sqrt(r1*r1 + r2*r2)

	fmt.Printf("Recovered state: x1 = %.8f, x2 = %.8f\n", x1, x2)
	fmt.Printf("Residual norm: %.8e\n", residualNorm)
}
