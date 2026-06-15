package main

import (
	"fmt"
	"math"
)

func factorial(n int) float64 {
	result := 1.0
	for i := 2; i <= n; i++ {
		result *= float64(i)
	}
	return result
}

func taylorExp(x float64, order int) float64 {
	total := 0.0
	for n := 0; n <= order; n++ {
		total += math.Pow(x, float64(n)) / factorial(n)
	}
	return total
}

func main() {
	xs := []float64{0.5, 1.0, 3.0}
	orders := []int{2, 10, 10}

	fmt.Println("method,function_name,center,x_value,order,approximation,reference_value,absolute_error,relative_error,warning")
	for i, x := range xs {
		order := orders[i]
		approximation := taylorExp(x, order)
		reference := math.Exp(x)
		absErr := math.Abs(reference - approximation)
		relErr := absErr / math.Abs(reference)
		warning := ""
		if math.Abs(x) > 2.0 {
			warning = "Evaluation is far from the expansion center; review local validity."
		}
		fmt.Printf("Maclaurin truncation,exp(x),0.0,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%s\n", x, order, approximation, reference, absErr, relErr, warning)
	}
}
