package main

import (
	"fmt"
	"math"
)

func emissions(t float64) float64 { return 50.0 * math.Exp(0.015*t) }
func emissionsRate(t float64) float64 { return 0.015 * emissions(t) }
func concentration(e float64) float64 { return 0.5 * e }
func forcing(c float64) float64 { return math.Log(1.0 + c) }

func main() {
	fmt.Println("t,emissions,concentration,forcing,temperature,emissions_rate,d_concentration_d_emissions,d_forcing_d_concentration,d_temperature_d_forcing,total_derivative")
	for _, t := range []float64{0.0, 5.0, 10.0, 20.0, 40.0} {
		e := emissions(t)
		c := concentration(e)
		f := forcing(c)
		temp := 1.2 * f
		s1 := emissionsRate(t)
		s2 := 0.5
		s3 := 1.0 / (1.0 + c)
		s4 := 1.2
		total := s4 * s3 * s2 * s1
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f\n", t, e, c, f, temp, s1, s2, s3, s4, total)
	}
}
