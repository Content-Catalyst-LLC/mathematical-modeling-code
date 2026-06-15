package main

import "fmt"

func main() {
	duration := []float64{1, 1, 1, 1, 1}
	inflow := []float64{12, 10, 9, 8, 7}
	outflow := []float64{6, 7, 8, 9, 9}
	exposure := []float64{20, 18, 15, 13, 11}
	population := []float64{1000, 1100, 1050, 980, 960}
	initialStock := 50.0

	cumulativeIn := 0.0
	cumulativeOut := 0.0
	cumulativeExposure := 0.0
	popExposure := 0.0

	for i := range duration {
		cumulativeIn += inflow[i] * duration[i]
		cumulativeOut += outflow[i] * duration[i]
		cumulativeExposure += exposure[i] * duration[i]
		popExposure += exposure[i] * population[i] * duration[i]
	}

	net := cumulativeIn - cumulativeOut
	endingStock := initialStock + net
	gross := cumulativeIn + cumulativeOut

	fmt.Println("initial_stock,cumulative_inflow,cumulative_outflow,net_accumulation,ending_stock,cumulative_exposure,population_weighted_exposure,gross_activity")
	fmt.Printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f\n", initialStock, cumulativeIn, cumulativeOut, net, endingStock, cumulativeExposure, popExposure, gross)
}
