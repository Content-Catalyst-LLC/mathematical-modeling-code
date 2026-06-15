package main

import "fmt"

func logisticDerivative(x, growth, carrying float64) float64 {
	return growth * (1 - 2*x/carrying)
}

func bistableRate(x, threshold float64) float64 {
	return x * (1 - x) * (x - threshold)
}

func numericalDerivative(x, threshold float64) float64 {
	h := 1e-5
	return (bistableRate(x+h, threshold) - bistableRate(x-h, threshold)) / (2 * h)
}

func classify(d float64) string {
	if d < -1e-8 {
		return "locally_stable"
	}
	if d > 1e-8 {
		return "locally_unstable"
	}
	return "inconclusive_by_linearization"
}

func main() {
	fmt.Println("scenario,equilibrium,derivative_value,stability,domain_min,domain_max,warning")
	for _, eq := range []float64{0, 100} {
		d := logisticDerivative(eq, 0.6, 100)
		fmt.Printf("logistic_growth,%.6f,%.6f,%s,0.000000,100.000000,Logistic stability assumes fixed carrying capacity and smooth density limitation.\n", eq, d, classify(d))
	}
	for _, eq := range []float64{0, 0.4, 1} {
		d := numericalDerivative(eq, 0.4)
		fmt.Printf("bistable_threshold,%.6f,%.6f,%s,0.000000,1.000000,Threshold stability depends on the assumed threshold and domain.\n", eq, d, classify(d))
	}
}
