package main

import "fmt"

func volume(h float64) float64 { return 12.0 * h * h }
func dVolumeDHeight(h float64) float64 { return 24.0 * h }
func heightPath(t float64) float64 { return 2.0 + 0.08*t }
func heightRate(t float64) float64 { return 0.08 }

func main() {
	fmt.Println("time,height,height_rate,volume,structural_derivative,inferred_volume_rate")
	for _, t := range []float64{0.0, 5.0, 10.0, 20.0, 40.0} {
		h := heightPath(t)
		hr := heightRate(t)
		v := volume(h)
		structural := dVolumeDHeight(h)
		inferred := structural * hr
		fmt.Printf("%.6f,%.12f,%.12f,%.12f,%.12f,%.12f\n", t, h, hr, v, structural, inferred)
	}
}
