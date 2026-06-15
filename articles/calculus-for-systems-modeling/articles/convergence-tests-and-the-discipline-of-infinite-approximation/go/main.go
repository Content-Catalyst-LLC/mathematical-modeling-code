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

func pSeriesSum(p float64, n int) float64 {
	total := 0.0
	for i := 1; i <= n; i++ {
		total += 1.0 / math.Pow(float64(i), p)
	}
	return total
}

func main() {
	geo := geometricSum(10.0, 0.6, 25)
	geoRef := 10.0 / (1.0 - 0.6)
	p125 := pSeriesSum(1.25, 10000)
	p075 := pSeriesSum(0.75, 10000)

	fmt.Println("series_name,test_used,n_terms,partial_sum,last_term,test_result,estimated_error")
	fmt.Printf("geometric_r_0.6,geometric-series test,25,%.12f,%.12f,converges by geometric-series test,%.12f\n", geo, 10.0*math.Pow(0.6, 24), geoRef-geo)
	fmt.Printf("p_series_1.25,p-series test,10000,%.12f,%.12f,converges,\n", p125, 1.0/math.Pow(10000.0, 1.25))
	fmt.Printf("p_series_0.75,p-series test,10000,%.12f,%.12f,diverges,\n", p075, 1.0/math.Pow(10000.0, 0.75))
}
