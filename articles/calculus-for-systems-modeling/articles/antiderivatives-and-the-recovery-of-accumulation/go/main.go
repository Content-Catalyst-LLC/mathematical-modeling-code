package main

import "fmt"

func netFlow(t float64) float64 { return (12.0 + 0.5*t) - (7.0 + 0.2*t) }

func main() {
	times := []float64{0, 1, 2, 3, 4, 5, 6}
	stock := 100.0
	fmt.Println("time,net_flow,recovered_stock,method")
	fmt.Printf("%.6f,%.12f,%.12f,initial condition\n", times[0], netFlow(times[0]), stock)
	for i := 1; i < len(times); i++ {
		previous := times[i-1]
		current := times[i]
		dt := current - previous
		stock += 0.5 * (netFlow(previous) + netFlow(current)) * dt
		fmt.Printf("%.6f,%.12f,%.12f,trapezoidal accumulation\n", current, netFlow(current), stock)
	}
}
