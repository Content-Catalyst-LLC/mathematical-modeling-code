package main

import (
	"fmt"
	"math"
)

func fModel(x float64, y float64) float64 { return x*x + x*y + 3.0*y*y + 0.2*x*x*y }
func gradient(x float64, y float64) (float64, float64) { return 2.0*x + y + 0.4*x*y, x + 6.0*y + 0.2*x*x }
func classify(h11 float64, h12 float64, h21 float64, h22 float64) string {
	det := h11*h22 - h12*h21
	if det > 0.0 && h11 > 0.0 { return "positive definite" }
	if det > 0.0 && h11 < 0.0 { return "negative definite" }
	if det < 0.0 { return "indefinite" }
	return "semidefinite or inconclusive"
}

func main() {
	cases := [][4]float64{{2.0,1.0,0.1,-0.05}, {2.0,1.0,0.5,0.5}, {-5.0,0.0,0.2,0.1}}
	fmt.Println("x,y,dx,dy,gradient_x,gradient_y,h11,h12,h21,h22,determinant,trace,classification,first_order_change,second_order_change,actual_change,first_order_error,second_order_error,warning")
	for _, row := range cases {
		x := row[0]; y := row[1]; dx := row[2]; dy := row[3]
		gx, gy := gradient(x,y)
		h11 := 2.0 + 0.4*y; h12 := 1.0 + 0.4*x; h21 := h12; h22 := 6.0
		det := h11*h22 - h12*h21
		cl := classify(h11,h12,h21,h22)
		first := gx*dx + gy*dy
		second := first + 0.5*(h11*dx*dx + 2.0*h12*dx*dy + h22*dy*dy)
		actual := fModel(x+dx,y+dy) - fModel(x,y)
		warning := ""
		if det < 0.0 { warning = "Hessian is indefinite; local structure is saddle-like." } else if math.Abs(det) < 1e-8 { warning = "Hessian is singular or nearly singular." }
		fmt.Printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n", x,y,dx,dy,gx,gy,h11,h12,h21,h22,det,h11+h22,cl,first,second,actual,math.Abs(actual-first),math.Abs(actual-second),warning)
	}
}
