package main

import "fmt"

type PopulationScenario struct {
	Key               string
	GrowthRate        float64
	CarryingCapacity  float64
	InitialPopulation float64
	Years             int
}

func logisticFinal(s PopulationScenario) float64 {
	population := s.InitialPopulation
	for year := 0; year < s.Years; year++ {
		population = population + s.GrowthRate*population*(1.0-population/s.CarryingCapacity)
	}
	return population
}

func main() {
	scenarios := []PopulationScenario{
		{"baseline", 0.28, 500.0, 40.0, 20},
		{"lower_growth", 0.18, 500.0, 40.0, 20},
		{"higher_growth", 0.38, 500.0, 40.0, 20},
		{"lower_capacity", 0.28, 350.0, 40.0, 20},
		{"higher_capacity", 0.28, 700.0, 40.0, 20},
	}

	fmt.Println("key,growth_rate,carrying_capacity,initial_population,years,final_population,crosses_capacity_midpoint")
	for _, s := range scenarios {
		finalValue := logisticFinal(s)
		crosses := finalValue >= s.CarryingCapacity/2.0
		fmt.Printf("%s,%.3f,%.3f,%.3f,%d,%.6f,%t\n", s.Key, s.GrowthRate, s.CarryingCapacity, s.InitialPopulation, s.Years, finalValue, crosses)
	}
}
