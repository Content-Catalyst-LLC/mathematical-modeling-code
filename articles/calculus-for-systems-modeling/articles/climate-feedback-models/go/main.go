package main

import (
	"fmt"
	"math"
)

func oneBox(forcing, feedback, heatCapacity, time float64) float64 {
	equilibrium := forcing / feedback
	return equilibrium * (1.0 - math.Exp(-(feedback/heatCapacity)*time))
}

func main() {
	forcing := 3.7
	c := 8.0
	fmt.Println("time,weak_feedback,baseline_feedback,strong_feedback")
	for t := 0; t <= 100; t += 10 {
		tf := float64(t)
		fmt.Printf("%d,%.6f,%.6f,%.6f\n", t, oneBox(forcing, 0.9, c, tf), oneBox(forcing, 1.2, c, tf), oneBox(forcing, 1.6, c, tf))
	}
}
