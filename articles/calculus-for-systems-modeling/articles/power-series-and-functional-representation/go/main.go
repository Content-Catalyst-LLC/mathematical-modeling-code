package main

import (
	"fmt"
	"math"
)

func geometricPowerSeries(x float64, nTerms int) float64 {
	total := 0.0
	for n := 0; n < nTerms; n++ {
		total += math.Pow(x, float64(n))
	}
	return total
}

func main() {
	xs := []float64{0.25, 0.75, 1.25}
	ns := []int{5, 20, 10}

	fmt.Println("function_name,center,x_value,n_terms,partial_sum,reference_value,absolute_error,convergence_status,warning")
	for i, x := range xs {
		nTerms := ns[i]
		partial := geometricPowerSeries(x, nTerms)
		if math.Abs(x) < 1.0 {
			reference := 1.0 / (1.0 - x)
			fmt.Printf("1/(1-x),0.0,%.12f,%d,%.12f,%.12f,%.12f,inside radius of convergence,\n", x, nTerms, partial, reference, math.Abs(reference-partial))
		} else {
			fmt.Printf("1/(1-x),0.0,%.12f,%d,%.12f,,,outside radius of convergence,Power series does not converge for this x value.\n", x, nTerms, partial)
		}
	}
}
