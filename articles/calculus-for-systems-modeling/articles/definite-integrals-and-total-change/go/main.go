package main

import (
	"fmt"
	"math"
)

func netRate(t float64) float64 { return 4.0*math.Sin(t/2.0) + 1.0 }

func main() {
	times := []float64{0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4}
	signedAccumulation := 0.0
	absoluteAccumulation := 0.0

	for i := 0; i < len(times)-1; i++ {
		dt := times[i+1] - times[i]
		r0 := netRate(times[i])
		r1 := netRate(times[i+1])
		signedAccumulation += 0.5 * (r0 + r1) * dt
		absoluteAccumulation += 0.5 * (math.Abs(r0) + math.Abs(r1)) * dt
	}

	fmt.Println("interval_start,interval_end,method,signed_accumulation,absolute_accumulation")
	fmt.Printf("%.6f,%.6f,trapezoidal approximation,%.12f,%.12f\n", times[0], times[len(times)-1], signedAccumulation, absoluteAccumulation)
}
