package main

import (
	"fmt"
	"math"
)

func gradient(x float64, y float64) (float64, float64) { return 2.0*x, 2.0*y }
func divergence(x float64, y float64) float64 { _ = x; _ = y; return 0.0 }
func curl2D(x float64, y float64) float64 { _ = x; _ = y; return 2.0 }

func audit(step float64, scenario string) {
	n := int(2.0/step) + 1
	count := 0
	gradSum := 0.0
	maxGrad := 0.0
	divSum := 0.0
	curlSum := 0.0
	maxAbsCurl := 0.0

	for i := 0; i < n; i++ {
		x := -1.0 + float64(i)*step
		for j := 0; j < n; j++ {
			y := -1.0 + float64(j)*step
			gx, gy := gradient(x, y)
			gmag := math.Sqrt(gx*gx + gy*gy)
			div := divergence(x, y)
			curl := curl2D(x, y)
			count++
			gradSum += gmag
			maxGrad = math.Max(maxGrad, gmag)
			divSum += div
			curlSum += curl
			maxAbsCurl = math.Max(maxAbsCurl, math.Abs(curl))
		}
	}

	warning := "Synthetic field-operator audit; document field definitions units grid and boundary rules."
	if step > 0.5 { warning = "Grid step is coarse; local derivative structure may be undersampled." }
	fmt.Printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,scalar f=x^2+y^2; vector F=<-y,x>,%s\n", scenario, step, count, gradSum/float64(count), maxGrad, divSum/float64(count), curlSum/float64(count), maxAbsCurl, warning)
}

func main() {
	fmt.Println("scenario,grid_step,point_count,mean_gradient_magnitude,maximum_gradient_magnitude,mean_divergence,mean_curl,maximum_abs_curl,field_description,warning")
	audit(1.0, "coarse_grid")
	audit(0.5, "medium_grid")
	audit(0.25, "fine_grid")
}
