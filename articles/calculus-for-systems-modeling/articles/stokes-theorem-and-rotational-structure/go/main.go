package main

import (
	"fmt"
	"math"
)

func audit(radius float64, segments int, radialSteps int, scenario string) {
	circulation := 0.0
	for i := 0; i < segments; i++ {
		theta0 := 2.0 * math.Pi * float64(i) / float64(segments)
		theta1 := 2.0 * math.Pi * float64(i+1) / float64(segments)
		x0, y0 := radius*math.Cos(theta0), radius*math.Sin(theta0)
		x1, y1 := radius*math.Cos(theta1), radius*math.Sin(theta1)
		xm, ym := 0.5*(x0+x1), 0.5*(y0+y1)
		dx, dy := x1-x0, y1-y0
		circulation += (-ym)*dx + xm*dy
	}

	curlFlux := 0.0
	for i := 0; i < radialSteps; i++ {
		r0 := radius * float64(i) / float64(radialSteps)
		r1 := radius * float64(i+1) / float64(radialSteps)
		ringArea := math.Pi * (r1*r1 - r0*r0)
		curlFlux += 2.0 * ringArea
	}

	warning := "Synthetic Stokes theorem audit."
	if segments < 64 || radialSteps < 16 { warning = "Coarse boundary or surface sampling." }
	fmt.Printf("%s,%.12f,%d,%d,%.12f,%.12f,%.12f,F=<-y,x,0>; curl F=<0,0,2>,horizontal disk with upward normal,counterclockwise boundary orientation viewed from positive z,%s\n", scenario, radius, segments, radialSteps, circulation, curlFlux, math.Abs(circulation-curlFlux), warning)
}

func main() {
	fmt.Println("scenario,radius,boundary_segments,radial_steps,boundary_circulation,surface_curl_flux,absolute_gap,field_description,surface_description,orientation_note,warning")
	audit(1.0, 32, 8, "coarse_audit")
	audit(1.0, 128, 32, "medium_audit")
	audit(1.0, 512, 128, "fine_audit")
}
