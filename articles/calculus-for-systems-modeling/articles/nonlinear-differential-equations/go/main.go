package main

import "fmt"

func logisticRate(x, growth, carrying float64) float64 {
	return growth * x * (1 - x/carrying)
}

func bistableRate(x, threshold float64) float64 {
	return x * (1 - x) * (x - threshold)
}

func main() {
	fmt.Println("scenario,time,state,rate,parameter_a,parameter_b,parameter_c,method,warning")
	dt := 0.05
	x := 10.0
	for n := 0; n <= 300; n++ {
		t := float64(n) * dt
		r := logisticRate(x, 0.6, 100)
		fmt.Printf("logistic_growth,%.6f,%.6f,%.6f,%.6f,%.6f,0.000000,explicit_euler,Logistic growth assumes a fixed carrying capacity and smooth density limitation.\n", t, x, r, 0.6, 100.0)
		x += dt * r
	}
	x = 0.35
	for n := 0; n <= 300; n++ {
		t := float64(n) * dt
		r := bistableRate(x, 0.4)
		fmt.Printf("bistable_threshold,%.6f,%.6f,%.6f,%.6f,0.000000,0.000000,explicit_euler,Threshold behavior is illustrative and should not be interpreted without evidence for the threshold.\n", t, x, r, 0.4)
		x += dt * r
	}
}
