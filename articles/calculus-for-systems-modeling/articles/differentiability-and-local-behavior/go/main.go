package main

import (
	"fmt"
	"math"
)

func smoothResponse(x float64) float64 {
	return math.Exp(0.2 * x)
}

func kinkResponse(x float64) float64 {
	return math.Abs(x)
}

func forwardDifference(f func(float64) float64, x float64, h float64) float64 {
	return (f(x+h) - f(x)) / h
}

func backwardDifference(f func(float64) float64, x float64, h float64) float64 {
	return (f(x) - f(x-h)) / h
}

func centralDifference(f func(float64) float64, x float64, h float64) float64 {
	return (f(x+h) - f(x-h)) / (2.0 * h)
}

func emit(name string, f func(float64) float64, x0 float64) {
	hValues := []float64{1.0, 0.5, 0.25, 0.125, 0.0625}

	for _, h := range hValues {
		fwd := forwardDifference(f, x0, h)
		bwd := backwardDifference(f, x0, h)
		cen := centralDifference(f, x0, h)
		gap := math.Abs(fwd - bwd)
		fmt.Printf("%s,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%t\n",
			name, x0, h, fwd, bwd, cen, gap, gap > 0.5)
	}
}

func main() {
	fmt.Println("function_name,x0,h,forward,backward,central,one_sided_gap,kink_flag")
	emit("smooth_exp_response", smoothResponse, 5.0)
	emit("kink_abs_response", kinkResponse, 0.0)
}
