package main

import "fmt"

func main() {
	a, b, c, d := 3.0, 1.0, 2.0, 4.0
	y1, y2 := 7.0, 8.0
	det := a*d - b*c

	if det == 0 {
		fmt.Println("Matrix is singular; recovery is not unique.")
		return
	}

	x1 := (d*y1 - b*y2) / det
	x2 := (-c*y1 + a*y2) / det

	fmt.Printf("Recovered state: x1 = %.2f, x2 = %.2f\n", x1, x2)
}
