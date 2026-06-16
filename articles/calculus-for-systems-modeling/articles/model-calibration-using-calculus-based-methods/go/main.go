package main

import (
	"fmt"
	"math"
)

func logistic(t, x0, r, k float64) float64 {
	return k / (1 + ((k-x0)/x0)*math.Exp(-r*t))
}
func main() {
	times := []float64{0, 2, 4, 6, 8, 10, 12}
	observed := []float64{10, 17.5, 29.2, 44.1, 60.5, 74.0, 83.2}
	rates := []float64{0.22, 0.26, 0.30, 0.34, 0.38, 0.42}
	caps := []float64{85, 95, 105, 115, 125}
	fmt.Println("growth_rate,carrying_capacity,loss,mean_absolute_residual,max_absolute_residual,warning")
	for _, r := range rates {
		for _, k := range caps {
			loss := 0.0
			absSum := 0.0
			maxAbs := 0.0
			for i, t := range times {
				pred := logistic(t, 10, r, k)
				res := observed[i] - pred
				ar := math.Abs(res)
				loss += res * res
				absSum += ar
				if ar > maxAbs { maxAbs = ar }
			}
			fmt.Printf("%.6f,%.6f,%.12f,%.12f,%.12f,Calibration fit does not prove model validity validation and sensitivity review remain required.\n", r, k, loss, absSum/float64(len(times)), maxAbs)
		}
	}
}
