package main

import "fmt"

func linearDecline(e0 float64, year int, years int) float64 {
	v := e0 * (1.0 - float64(year)/float64(years))
	if v < 0 {
		return 0
	}
	return v
}

func main() {
	e0 := 40.0
	years := 30
	cumulative := 0.0
	for y := 0; y <= years; y++ {
		cumulative += linearDecline(e0, y, years)
	}
	fmt.Println("scenario_name,pathway_type,cumulative_emissions,warning")
	fmt.Printf("linear_decline_to_zero,linear_decline,%.6f,linear_decline_still_accumulates_until_net_zero\n", cumulative)
}
