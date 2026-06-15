package main

import (
	"fmt"
	"math"
)

func forcingFunction(t, amplitude, frequency float64) float64 {
	return amplitude * math.Cos(frequency*t)
}

func acceleration(x, v, t, damping, natural, forceAmp, forceFreq float64) float64 {
	return forcingFunction(t, forceAmp, forceFreq) - 2*damping*natural*v - natural*natural*x
}

func simulate(scenario string, damping, forceAmp float64) {
	x := 1.0
	v := 0.0
	natural := 1.0
	forceFreq := 1.0
	dt := 0.02
	for n := 0; n <= 500; n++ {
		t := float64(n) * dt
		a := acceleration(x, v, t, damping, natural, forceAmp, forceFreq)
		force := forcingFunction(t, forceAmp, forceFreq)
		fmt.Printf("%s,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,explicit_euler_first_order_system,Explicit Euler is transparent but can distort oscillatory systems if the step size is too large.\n", scenario, t, x, v, a, damping, natural, force)
		v += dt * a
		x += dt * v
	}
}

func main() {
	fmt.Println("scenario,time,position,velocity,acceleration,damping_ratio,natural_frequency,forcing,method,warning")
	simulate("underdamped_unforced", 0.2, 0.0)
	simulate("forced_near_resonance", 0.1, 0.2)
}
