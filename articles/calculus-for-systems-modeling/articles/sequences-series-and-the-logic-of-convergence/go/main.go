package main

import (
	"fmt"
	"math"
)

func geometricSum(a float64, r float64, n int) float64 {
	total := 0.0
	for i := 0; i < n; i++ {
		total += a * math.Pow(r, float64(i))
	}
	return total
}

func harmonicSum(n int) float64 {
	total := 0.0
	for i := 1; i <= n; i++ {
		total += 1.0 / float64(i)
	}
	return total
}

func main() {
	geo := geometricSum(10.0, 0.6, 25)
	geoRef := 10.0 / (1.0 - 0.6)
	harm := harmonicSum(10000)
	fmt.Println("series_name,n_terms,last_term,partial_sum,reference_value,estimated_error,convergence_classification")
	fmt.Printf("geometric_r_0.6,25,%.12f,%.12f,%.12f,%.12f,convergent geometric series\n", 10.0*math.Pow(0.6, 24), geo, geoRef, geoRef-geo)
	fmt.Printf("harmonic,10000,%.12f,%.12f,,,divergent despite terms approaching zero\n", 1.0/10000.0, harm)
}
