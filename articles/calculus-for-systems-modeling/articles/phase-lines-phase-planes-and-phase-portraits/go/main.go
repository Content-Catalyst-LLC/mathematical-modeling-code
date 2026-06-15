package main

import (
	"fmt"
	"math"
)

func rates(x, y, alpha, beta, delta, gamma float64) (float64, float64) {
	return alpha*x - beta*x*y, delta*x*y - gamma*y
}

func main() {
	alpha := 0.7
	beta := 0.05
	delta := 0.02
	gamma := 0.5
	fmt.Println("x,y,dxdt,dydt,x_nullcline_residual,y_nullcline_residual,speed,warning")
	for xi := 0; xi <= 60; xi += 5 {
		for yi := 0; yi <= 30; yi += 3 {
			x := float64(xi)
			y := float64(yi)
			dxdt, dydt := rates(x, y, alpha, beta, delta, gamma)
			speed := math.Sqrt(dxdt*dxdt + dydt*dydt)
			fmt.Printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Vector-field values depend on parameter values state ranges and the assumed interaction structure.\n", x, y, dxdt, dydt, dxdt, dydt, speed)
		}
	}
}
