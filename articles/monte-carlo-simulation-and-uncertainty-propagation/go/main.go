package main

import "fmt"

type LCG struct {
	state uint64
}

func (r *LCG) next() float64 {
	r.state = 6364136223846793005*r.state + 1
	return float64(r.state>>11) / float64(uint64(1)<<53)
}

func uniform(r *LCG, min float64, max float64) float64 {
	return min + r.next()*(max-min)
}

func runOnce(r *LCG) float64 {
	stock := uniform(r, 65.0, 75.0)
	growthRate := uniform(r, 0.14, 0.22)
	extraction := uniform(r, 5.0, 8.0)
	shockProbability := uniform(r, 0.02, 0.08)
	shockFraction := 0.12
	capacity := 100.0

	for step := 0; step < 50; step++ {
		growth := growthRate * stock * (1.0 - stock/capacity)
		shock := 0.0
		if r.next() < shockProbability {
			shock = stock * shockFraction
		}
		stock = stock + growth - extraction - shock
		if stock < 0 {
			stock = 0
		}
	}
	return stock
}

func main() {
	r := LCG{state: 20260612}
	replications := 1000
	sum := 0.0
	depleted := 0

	for i := 0; i < replications; i++ {
		finalStock := runOnce(&r)
		sum += finalStock
		if finalStock <= 10.0 {
			depleted++
		}
	}

	fmt.Printf("replications=%d mean_final_stock=%.6f depletion_probability=%.6f\n",
		replications, sum/float64(replications), float64(depleted)/float64(replications))
}
