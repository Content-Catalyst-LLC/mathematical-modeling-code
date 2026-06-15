package main

import (
	"fmt"
	"math"
)

func exposureField(x float64, y float64) float64 { return 10.0 + 2.0*x + 0.5*y*y }
func populationDensity(x float64, y float64) float64 { return 100.0 + 10.0*y + 5.0*math.Sin(x) }
func inRegion(x float64, y float64) bool { return x*x + y*y <= 9.0 }

func compute(step float64, scenario string) {
	n := int(6.0 / step)
	cellArea := step * step
	cells := 0
	totalDensity := 0.0
	totalPopulation := 0.0
	populationBurden := 0.0

	for i := 0; i <= n; i++ {
		x := -3.0 + float64(i)*step
		for j := 0; j <= n; j++ {
			y := -3.0 + float64(j)*step
			if inRegion(x, y) {
				exposure := exposureField(x, y)
				population := populationDensity(x, y)
				cells++
				totalDensity += exposure * cellArea
				totalPopulation += population * cellArea
				populationBurden += exposure * population * cellArea
			}
		}
	}

	totalArea := float64(cells) * cellArea
	warning := "Synthetic grid audit; region mask cell area and units should be documented."
	if step > 0.5 { warning = "Grid resolution is coarse; spatial accumulation may smooth local variation." }
	fmt.Printf("%s,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n", scenario, cells, cellArea, totalArea, totalDensity, totalDensity/totalArea, populationBurden, totalPopulation, populationBurden/totalPopulation, warning)
}

func main() {
	fmt.Println("scenario,cells_in_region,cell_area,total_area,total_density_accumulation,area_weighted_average,population_weighted_burden,population_total,population_weighted_average_exposure,warning")
	compute(1.0, "coarse_grid")
	compute(0.5, "medium_grid")
	compute(0.25, "fine_grid")
}
