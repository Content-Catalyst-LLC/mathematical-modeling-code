package main

import (
	"fmt"
	"math/rand"
)

func main() {
	const n = 10000
	rng := rand.New(rand.NewSource(42))

	total := 0.0

	for i := 0; i < n; i++ {
		exposure := 0.2 + 0.8*rng.Float64()
		vulnerability := rng.Float64()
		loss := exposure * vulnerability
		total += loss
	}

	fmt.Printf("Monte Carlo mean loss estimate: %.8f\n", total/float64(n))
}
