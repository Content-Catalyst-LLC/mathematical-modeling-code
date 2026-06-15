package main

import (
	"fmt"
	"math"
)

func height(x float64, y float64) float64 { return 0.1*x*x + 0.05*y*y }
func scalarField(x float64, y float64, z float64) float64 { _ = x; _ = y; return 1.0 + 0.2*z }
func vectorField(x float64, y float64, z float64) (float64, float64, float64) { _ = z; return 0.1*x, 0.1*y, 1.0 }
func normalAreaVector(x float64, y float64, step float64) (float64, float64, float64) {
	area := step * step
	return -0.2*x*area, -0.1*y*area, area
}
func norm3(x float64, y float64, z float64) float64 { return math.Sqrt(x*x + y*y + z*z) }
func dot3(ax float64, ay float64, az float64, bx float64, by float64, bz float64) float64 {
	return ax*bx + ay*by + az*bz
}

func audit(step float64, scenario string) {
	n := int(2.0 / step)
	count := 0
	surfaceArea := 0.0
	scalarTotal := 0.0
	fluxTotal := 0.0
	fluxDensitySum := 0.0
	maxPatch := 0.0

	for i := 0; i < n; i++ {
		x := -1.0 + float64(i)*step
		for j := 0; j < n; j++ {
			y := -1.0 + float64(j)*step
			z := height(x, y)
			ax, ay, az := normalAreaVector(x, y, step)
			vx, vy, vz := vectorField(x, y, z)
			patchArea := norm3(ax, ay, az)
			flux := dot3(vx, vy, vz, ax, ay, az)
			count++
			surfaceArea += patchArea
			scalarTotal += scalarField(x, y, z) * patchArea
			fluxTotal += flux
			fluxDensitySum += flux / math.Max(patchArea, 1e-12)
			maxPatch = math.Max(maxPatch, patchArea)
		}
	}

	warning := "Synthetic surface-integral audit; document surface normal units and mesh."
	if step > 0.5 { warning = "Grid step is coarse; curvature and field variation may be undersampled." }
	fmt.Printf("%s,%.12f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,graph z=0.1x^2+0.05y^2,%s\n", scenario, step, count, surfaceArea, scalarTotal, fluxTotal, fluxDensitySum/float64(count), maxPatch, warning)
}

func main() {
	fmt.Println("scenario,grid_step,patch_count,approximate_surface_area,scalar_surface_integral,vector_flux_integral,average_flux_density,maximum_patch_area,surface_description,warning")
	audit(1.0, "coarse_surface_mesh")
	audit(0.5, "medium_surface_mesh")
	audit(0.25, "fine_surface_mesh")
}
