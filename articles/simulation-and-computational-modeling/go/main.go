package main

import "fmt"

func main() {
	stock := 70.0
	growthRate := 0.18
	capacity := 100.0
	extraction := 6.0
	steps := 20

	fmt.Println("step,resource_stock")
	for step := 0; step <= steps; step++ {
		fmt.Printf("%d,%.6f\n", step, stock)
		growth := growthRate * stock * (1.0 - stock/capacity)
		stock = stock + growth - extraction
		if stock < 0 {
			stock = 0
		}
	}
}
