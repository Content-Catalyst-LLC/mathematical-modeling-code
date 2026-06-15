package main

import (
	"fmt"
	"math"
)

func response(x float64) float64 { return math.Exp(0.2*x) }
func exact(x float64) float64 { return 0.2*math.Exp(0.2*x) }
func avg(a float64,b float64) float64 { return (response(b)-response(a))/(b-a) }
func fwd(x float64,h float64) float64 { return (response(x+h)-response(x))/h }
func bwd(x float64,h float64) float64 { return (response(x)-response(x-h))/h }
func cen(x float64,h float64) float64 { return (response(x+h)-response(x-h))/(2*h) }
func elast(d float64,x float64) float64 { return (x/response(x))*d }

func main() {
	x := 5.0
	ex := exact(x)
	hs := []float64{1.0,0.5,0.25,0.125,0.0625}
	fmt.Println("method,x0,h,estimate,exact,absolute_error,elasticity")
	for _, h := range hs {
		rows := map[string]float64{
			"average_rate_right": avg(x,x+h),
			"forward_difference": fwd(x,h),
			"backward_difference": bwd(x,h),
			"central_difference": cen(x,h),
		}
		for m, e := range rows {
			fmt.Printf("%s,%.6f,%.6f,%.12f,%.12f,%.12f,%.12f\n", m, x, h, e, ex, math.Abs(e-ex), elast(e,x))
		}
	}
}
