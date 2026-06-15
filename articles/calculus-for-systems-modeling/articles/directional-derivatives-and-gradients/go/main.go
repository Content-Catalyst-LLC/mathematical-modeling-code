package main

import (
	"fmt"
	"math"
)

func f(x float64, y float64) float64 { return 3.0*x + 2.0*y + 0.5*x*y }
func gx(x float64, y float64) float64 { return 3.0 + 0.5*y }
func gy(x float64, y float64) float64 { return 2.0 + 0.5*x }
func normalize(vx float64, vy float64) (float64, float64) {
	norm := math.Sqrt(vx*vx + vy*vy)
	if norm == 0 { panic("Direction vector must be nonzero.") }
	return vx / norm, vy / norm
}
func directionalDerivative(x float64, y float64, ux float64, uy float64) float64 { return gx(x,y)*ux + gy(x,y)*uy }
func feasibleDirection(x float64, y float64, ux float64, uy float64, step float64) bool { return x >= 0.0 && y >= 0.0 && x+y <= 10.0 && x+step*ux >= 0.0 && y+step*uy >= 0.0 && x+step*ux+y+step*uy <= 10.0 }

func main() {
	cases := [][5]float64{{4.0,3.0,1.0,1.0,0.25}, {4.0,3.0,2.0,-1.0,0.25}, {8.0,1.0,1.0,1.0,1.0}}
	fmt.Println("x,y,direction_x,direction_y,unit_x,unit_y,gradient_x,gradient_y,directional_derivative,step_size,estimated_change,actual_change,absolute_error,feasible_direction,warning")
	for _, row := range cases {
		x := row[0]; y := row[1]; vx := row[2]; vy := row[3]; step := row[4]
		ux, uy := normalize(vx, vy)
		deriv := directionalDerivative(x,y,ux,uy)
		estimated := step * deriv
		actual := f(x+step*ux, y+step*uy) - f(x,y)
		feasible := feasibleDirection(x,y,ux,uy,step)
		warning := ""
		if !feasible { warning = "Direction and step move outside the feasible region." }
		fmt.Printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%t,%s\n", x,y,vx,vy,ux,uy,gx(x,y),gy(x,y),deriv,step,estimated,actual,math.Abs(actual-estimated),feasible,warning)
	}
}
