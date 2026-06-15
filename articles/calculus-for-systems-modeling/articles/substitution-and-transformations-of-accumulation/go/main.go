package main

import (
	"fmt"
	"math"
)

func g(x float64) float64 { return x*x + 1.0 }
func gPrime(x float64) float64 { return 2.0 * x }
func f(u float64) float64 { return math.Sqrt(u) }
func integrandX(x float64) float64 { return f(g(x)) * gPrime(x) }

func trap(fn func(float64) float64, a float64, b float64, n int) float64 {
	step := (b - a) / float64(n)
	total := 0.0
	for i := 0; i < n; i++ {
		x0 := a + step*float64(i)
		x1 := x0 + step
		total += 0.5 * (fn(x0) + fn(x1)) * step
	}
	return total
}

func main() {
	a := 1.0
	b := 3.0
	ua := g(a)
	ub := g(b)
	direct := trap(integrandX, a, b, 400)
	transformed := trap(f, ua, ub, 400)
	residual := direct - transformed

	fmt.Println("original_start,original_end,transformed_start,transformed_end,direct_integral,transformed_integral,residual")
	fmt.Printf("%.6f,%.6f,%.6f,%.6f,%.12f,%.12f,%.12f\n", a, b, ua, ub, direct, transformed, residual)
}
