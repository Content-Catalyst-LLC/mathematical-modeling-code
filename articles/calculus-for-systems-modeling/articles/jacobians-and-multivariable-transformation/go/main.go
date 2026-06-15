package main

import (
	"fmt"
	"math"
)

func fModel(x float64, y float64) (float64, float64) { return x*x + y, x*y + 3.0*y }

func main() {
	cases := [][4]float64{{2.0,1.0,0.1,-0.05}, {2.0,1.0,0.5,0.5}, {0.0,0.0,0.1,0.1}}
	fmt.Println("x,y,dx,dy,j11,j12,j21,j22,determinant,approximate_change_1,approximate_change_2,actual_change_1,actual_change_2,error_norm,warning")
	for _, row := range cases {
		x := row[0]; y := row[1]; dx := row[2]; dy := row[3]
		j11 := 2.0*x; j12 := 1.0; j21 := y; j22 := x + 3.0
		b1,b2 := fModel(x,y)
		a1,a2 := fModel(x+dx,y+dy)
		ac1 := j11*dx + j12*dy
		ac2 := j21*dx + j22*dy
		rc1 := a1 - b1
		rc2 := a2 - b2
		det := j11*j22 - j12*j21
		err := math.Sqrt((rc1-ac1)*(rc1-ac1) + (rc2-ac2)*(rc2-ac2))
		warning := ""
		if math.Abs(det) <= 1e-8 { warning = "Jacobian is singular or near singular." }
		fmt.Printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%s\n", x,y,dx,dy,j11,j12,j21,j22,det,ac1,ac2,rc1,rc2,err,warning)
	}
}
