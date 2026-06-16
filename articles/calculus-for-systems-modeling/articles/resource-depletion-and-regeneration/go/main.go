package main

import "fmt"

func logisticRegeneration(stock, r, k float64) float64 {
	v := r * stock * (1.0 - stock/k)
	if v < 0 {
		return 0
	}
	return v
}

func main() {
	stock := 600.0
	harvest := 35.0
	dt := 0.1
	cumulative := 0.0
	for i := 0; i < 800; i++ {
		extraction := harvest * dt
		if extraction > stock {
			extraction = stock
		}
		growth := logisticRegeneration(stock, 0.18, 1000.0) * dt
		stock = stock + growth - extraction
		if stock < 0 {
			stock = 0
		}
		cumulative += extraction
	}
	fmt.Println("scenario_name,resource_type,final_stock,cumulative_extraction,warning")
	fmt.Printf("renewable_precautionary_harvest,renewable_logistic,%.6f,%.6f,precautionary_harvest\n", stock, cumulative)
}
