package main

import (
	"fmt"
	"math"
)

func f(x float64, y float64) float64 { return 3.0*x + 2.0*y + 0.5*x*y }
func fx(x float64, y float64) float64 { return 3.0 + 0.5*y }
func fy(x float64, y float64) float64 { return 2.0 + 0.5*x }
func totalDifferential(x float64, y float64, dx float64, dy float64) float64 { return fx(x,y)*dx + fy(x,y)*dy }
func feasibleDisplacement(x float64, y float64, dx float64, dy float64) bool { return x >= 0.0 && y >= 0.0 && x+y <= 10.0 && x+dx >= 0.0 && y+dy >= 0.0 && x+dx+y+dy <= 10.0 }

func main() {
	cases := [][4]float64{{4.0,3.0,0.2,-0.1}, {4.0,3.0,1.0,1.0}, {8.0,1.0,1.0,1.0}}
	fmt.Println("x,y,dx,dy,baseline_output,actual_output,actual_change,differential_estimate,absolute_error,feasible_displacement,warning")
	for _, row := range cases {
		x := row[0]; y := row[1]; dx := row[2]; dy := row[3]
		baseline := f(x,y)
		actual := f(x+dx,y+dy)
		change := actual - baseline
		estimate := totalDifferential(x,y,dx,dy)
		feasible := feasibleDisplacement(x,y,dx,dy)
		warning := ""
		if !feasible { warning = "Displacement is outside the feasible region." }
		fmt.Printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%t,%s\n", x, y, dx, dy, baseline, actual, change, estimate, math.Abs(change-estimate), feasible, warning)
	}
}
