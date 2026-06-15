package main

import (
	"fmt"
	"math"
)

func u(x float64) float64 { return 1.0 + x }
func uPrime(x float64) float64 { return 1.0 }
func v(x float64) float64 { return math.Exp(-0.3*x) * math.Sin(x) }
func vPrime(x float64) float64 { return math.Exp(-0.3*x) * (math.Cos(x) - 0.3*math.Sin(x)) }
func directIntegrand(x float64) float64 { return u(x) * vPrime(x) }
func residualIntegrand(x float64) float64 { return v(x) * uPrime(x) }

func trap(fn func(float64) float64, a float64, b float64, n int) float64 {
	dx := (b - a) / float64(n)
	total := 0.0
	for i := 0; i < n; i++ {
		x0 := a + dx*float64(i)
		x1 := x0 + dx
		total += 0.5 * (fn(x0) + fn(x1)) * dx
	}
	return total
}

func main() {
	a := 0.0
	b := 4.0
	direct := trap(directIntegrand, a, b, 800)
	residual := trap(residualIntegrand, a, b, 800)
	boundary := u(b)*v(b) - u(a)*v(a)
	decomposed := boundary - residual
	decompResid := direct - decomposed

	fmt.Println("interval_start,interval_end,direct_integral,boundary_term,residual_integral,decomposed_value,decomposition_residual")
	fmt.Printf("%.6f,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n", a, b, direct, boundary, residual, decomposed, decompResid)
}
