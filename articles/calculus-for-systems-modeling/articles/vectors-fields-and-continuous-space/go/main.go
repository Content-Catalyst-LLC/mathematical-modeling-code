package main

import (
	"fmt"
	"math"
)

func scalarField(x float64, y float64) float64 {
	return 20.0 + 2.0*math.Sin(x) + 0.5*y*y
}

func vectorField(x float64, y float64) (float64, float64) {
	return -y, x
}

func vectorMagnitude(vx float64, vy float64) float64 {
	return math.Sqrt(vx*vx + vy*vy)
}

func audit(step float64, scenario string) {
	n := int(6.0 / step)
	count := 0
	scalarSum := 0.0
	scalarMin := math.Inf(1)
	scalarMax := math.Inf(-1)
	magSum := 0.0
	magMax := 0.0

	for i := 0; i <= n; i++ {
		x := -3.0 + float64(i)*step
		for j := 0; j <= n; j++ {
			y := -3.0 + float64(j)*step
			s := scalarField(x, y)
			vx, vy := vectorField(x, y)
			mag := vectorMagnitude(vx, vy)
			count++
			scalarSum += s
			scalarMin = math.Min(scalarMin, s)
			scalarMax = math.Max(scalarMax, s)
			magSum += mag
			magMax = math.Max(magMax, mag)
		}
	}

	warning := "Synthetic field audit; document domain units and interpolation assumptions."
	if step > 0.75 { warning = "Grid resolution is coarse; field structure may be undersampled." }
	fmt.Printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,square domain [-3,3] x [-3,3],%s\n", scenario, step, count, scalarSum/float64(count), scalarMin, scalarMax, magSum/float64(count), magMax, warning)
}

func main() {
	fmt.Println("scenario,grid_step,point_count,scalar_average,scalar_minimum,scalar_maximum,vector_magnitude_average,vector_magnitude_maximum,domain_description,warning")
	audit(1.0, "coarse_grid")
	audit(0.5, "medium_grid")
	audit(0.25, "fine_grid")
}
