package main

import (
	"fmt"
	"math"
)

func vectorField(x float64, y float64) (float64, float64) { return -y, x }
func dot(ax float64, ay float64, bx float64, by float64) float64 { return ax*bx + ay*by }

func audit(radius float64, segments int, scenario string) {
	fluxTotal := 0.0
	circulationTotal := 0.0
	tangentSum := 0.0
	normalSum := 0.0

	for i := 0; i < segments; i++ {
		theta0 := 2.0 * math.Pi * float64(i) / float64(segments)
		theta1 := 2.0 * math.Pi * float64(i+1) / float64(segments)
		x0, y0 := radius*math.Cos(theta0), radius*math.Sin(theta0)
		x1, y1 := radius*math.Cos(theta1), radius*math.Sin(theta1)
		xm, ym := 0.5*(x0+x1), 0.5*(y0+y1)
		dx, dy := x1-x0, y1-y0
		segmentLength := math.Sqrt(dx*dx + dy*dy)
		tx, ty := dx/segmentLength, dy/segmentLength
		nx, ny := xm/radius, ym/radius
		fx, fy := vectorField(xm, ym)

		circulationTotal += dot(fx, fy, dx, dy)
		fluxTotal += dot(fx, fy, nx, ny) * segmentLength
		tangentSum += dot(fx, fy, tx, ty)
		normalSum += dot(fx, fy, nx, ny)
	}

	warning := "Synthetic flow audit; document field meaning orientation units and boundary choice."
	if segments < 32 { warning = "Coarse path sampling; circulation and flux should be checked with more segments." }
	fmt.Printf("%s,%d,%.12f,%.12f,%.12f,%.12f,rotating field F=<-y,x>,counterclockwise circle with radius 1,%s\n", scenario, segments, fluxTotal, circulationTotal, tangentSum/float64(segments), normalSum/float64(segments), warning)
}

func main() {
	fmt.Println("scenario,segment_count,approximate_flux,approximate_circulation,mean_tangential_alignment,mean_normal_alignment,field_description,geometry_description,warning")
	audit(1.0, 16, "coarse_circle")
	audit(1.0, 64, "medium_circle")
	audit(1.0, 256, "fine_circle")
}
