package main

import (
	"fmt"
	"math"
)

func objective(x float64, y float64) float64 { return x*x + 2.0*y*y }

func main() {
	targets := []float64{12.0, 18.0, 24.0}
	fmt.Println("x,y,objective_value,constraint_value,constraint_target,constraint_residual,lambda_value,gradient_f_x,gradient_f_y,gradient_g_x,gradient_g_y,stationarity_residual_norm,feasible,warning")
	for _, target := range targets {
		y := target / 3.0
		x := 2.0 * target / 3.0
		lambda := 2.0 * x
		gfx := 2.0 * x
		gfy := 4.0 * y
		ggx := 1.0
		ggy := 1.0
		sx := gfx - lambda*ggx
		sy := gfy - lambda*ggy
		norm := math.Sqrt(sx*sx + sy*sy)
		cval := x + y
		cres := cval - target
		feasible := math.Abs(cres) <= 1e-9
		warning := "Review feasibility or stationarity."
		if feasible && norm <= 1e-8 { warning = "Multiplier interpretation is local and unit-dependent." }
		fmt.Printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%t,%s\n", x,y,objective(x,y),cval,target,cres,lambda,gfx,gfy,ggx,ggy,norm,feasible,warning)
	}
}
