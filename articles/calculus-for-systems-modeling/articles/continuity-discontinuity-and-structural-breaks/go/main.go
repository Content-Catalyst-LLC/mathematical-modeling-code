package main

import (
	"fmt"
	"math"
)

func piecewiseSystem(x float64) float64 {
	if x < 5.0 {
		return 2.0 + 0.5*x
	}
	return 6.0 + 1.4*(x-5.0)
}

func classify(levelJump float64, slopeChange float64) string {
	if levelJump > 1.0 && slopeChange > 0.5 {
		return "level_and_slope_break"
	}
	if levelJump > 1.0 {
		return "possible_jump"
	}
	if slopeChange > 0.5 {
		return "possible_slope_break"
	}
	return "ok"
}

func main() {
	xs := make([]float64, 41)
	ys := make([]float64, 41)

	for i := 0; i <= 40; i++ {
		xs[i] = float64(i) * 0.25
		ys[i] = piecewiseSystem(xs[i])
	}

	fmt.Println("x,y,left_slope,right_slope,slope_change,level_jump,flag")

	for i := 0; i < len(xs); i++ {
		if i == 0 || i == len(xs)-1 {
			fmt.Printf("%.6f,%.6f,,,,,ok\n", xs[i], ys[i])
		} else {
			leftSlope := (ys[i] - ys[i-1]) / (xs[i] - xs[i-1])
			rightSlope := (ys[i+1] - ys[i]) / (xs[i+1] - xs[i])
			slopeChange := math.Abs(rightSlope - leftSlope)
			levelJump := math.Abs(ys[i] - ys[i-1])
			fmt.Printf("%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%s\n",
				xs[i], ys[i], leftSlope, rightSlope, slopeChange, levelJump, classify(levelJump, slopeChange))
		}
	}
}
