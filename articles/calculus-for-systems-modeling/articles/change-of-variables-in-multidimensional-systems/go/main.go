package main

import (
	"fmt"
	"math"
)

func exposureCartesian(x float64, y float64) float64 {
	r := math.Sqrt(x*x + y*y)
	return 20.0 * math.Exp(-0.4*r)
}

func exposurePolar(r float64, theta float64) float64 {
	_ = theta
	return 20.0 * math.Exp(-0.4*r)
}

func polarTotal(radius float64, dr float64, dtheta float64) float64 {
	total := 0.0
	for r := dr / 2.0; r < radius; r += dr {
		for theta := dtheta / 2.0; theta < 2.0*math.Pi; theta += dtheta {
			total += exposurePolar(r, theta) * r * dr * dtheta
		}
	}
	return total
}

func cartesianGridTotal(radius float64, step float64) float64 {
	total := 0.0
	n := int((2.0 * radius) / step)
	for i := 0; i <= n; i++ {
		x := -radius + float64(i)*step
		for j := 0; j <= n; j++ {
			y := -radius + float64(j)*step
			if x*x+y*y <= radius*radius {
				total += exposureCartesian(x, y) * step * step
			}
		}
	}
	return total
}

func audit(radius float64, dr float64, dtheta float64, scenario string) {
	p := polarTotal(radius, dr, dtheta)
	c := cartesianGridTotal(radius, dr)
	diff := math.Abs(p - c)
	rel := diff / math.Max(math.Abs(p), 1e-12)
	warning := "Polar Jacobian factor r included; compare domain and resolution assumptions."
	if dr > 0.5 { warning = "Resolution is coarse; transformed and Cartesian approximations may differ." }
	fmt.Printf("%s,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,dA = r dr dtheta,%s\n", scenario, radius, dr, dtheta, p, c, diff, rel, warning)
}

func main() {
	fmt.Println("scenario,radius,radial_step,angular_step,polar_total,cartesian_grid_total,absolute_difference,relative_difference,jacobian_rule,warning")
	audit(3.0, 0.5, math.Pi/24.0, "medium_polar_grid")
	audit(3.0, 0.25, math.Pi/48.0, "fine_polar_grid")
	audit(3.0, 0.125, math.Pi/96.0, "very_fine_polar_grid")
}
