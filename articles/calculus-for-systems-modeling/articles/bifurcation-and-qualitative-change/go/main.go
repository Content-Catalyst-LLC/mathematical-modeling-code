package main

import (
	"fmt"
	"math"
)

func classify(d float64) string {
	if d < -1e-8 {
		return "locally_stable"
	}
	if d > 1e-8 {
		return "locally_unstable"
	}
	return "inconclusive_at_critical_value"
}

func main() {
	fmt.Println("model,parameter_mu,equilibrium,derivative_value,stability,branch_status,warning")
	for step := -20; step <= 40; step++ {
		mu := float64(step) / 10.0
		if mu < 0 {
			fmt.Printf("saddle_node_normal_form,%.6f,,,no_real_equilibrium,equilibrium_absent,For mu below zero the saddle-node normal form has no real equilibrium.\n", mu)
		} else if math.Abs(mu) < 1e-12 {
			eq := 0.0
			d := -2.0 * eq
			fmt.Printf("saddle_node_normal_form,%.6f,%.6f,%.6f,%s,critical_branch,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n", mu, eq, d, classify(d))
		} else {
			root := math.Sqrt(mu)
			for _, eq := range []float64{-root, root} {
				d := -2.0 * eq
				fmt.Printf("saddle_node_normal_form,%.6f,%.6f,%.6f,%s,equilibrium_present,Bifurcation interpretation depends on model form parameter meaning and domain validity.\n", mu, eq, d, classify(d))
			}
		}
	}
}
