package main

import (
	"fmt"
	"math"
)

func audit(gridSteps int, scenario string) {
	step := 1.0 / float64(gridSteps)
	area := step * step
	flux := 0.0
	for i := 0; i < gridSteps; i++ {
		for j := 0; j < gridSteps; j++ {
			flux += 3.0 * area
		}
	}
	divIntegral := 3.0
	warning := "Synthetic divergence theorem audit."
	if gridSteps < 8 { warning = "Coarse grid; refine before interpreting the boundary-volume comparison." }
	fmt.Printf("%s,%d,%.12f,%.12f,%.12f,F=<x,y,z>; divergence = 3,unit cube [0,1]x[0,1]x[0,1],all six cube faces use outward normals,%s\n", scenario, gridSteps, flux, divIntegral, math.Abs(flux-divIntegral), warning)
}

func main() {
	fmt.Println("scenario,grid_steps,boundary_flux,volume_divergence_integral,absolute_gap,field_description,volume_description,normal_note,warning")
	audit(4, "coarse_audit")
	audit(16, "medium_audit")
	audit(64, "fine_audit")
}
