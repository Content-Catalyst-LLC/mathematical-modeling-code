package main

import (
	"fmt"
	"math"
)

func logistic(t, x0, r, k float64) float64 {
	return k / (1 + ((k-x0)/x0)*math.Exp(-r*t))
}
func main() {
	rates := []float64{0.18, 0.25, 0.35, 0.45, 0.55}
	caps := []float64{80, 100, 125, 150}
	fmt.Println("growth_rate,carrying_capacity,initial_value,stop_time,final_value,output_metric,warning")
	for _, r := range rates {
		for _, k := range caps {
			fmt.Printf("%.6f,%.6f,10.000000,20.000000,%.12f,final_state_value,Sweep results depend on tested ranges baseline assumptions and model structure.\n", r, k, logistic(20, 10, r, k))
		}
	}
}
