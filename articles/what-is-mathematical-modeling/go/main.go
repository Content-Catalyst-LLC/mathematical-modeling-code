package main

import (
	"fmt"
	"math"
)

type LogisticModel struct {
	Name             string
	InitialState     float64
	GrowthRate       float64
	CarryingCapacity float64
	Dt               float64
	Steps            int
}

func derivative(x, r, k float64) float64 {
	return r * x * (1.0 - x/k)
}

func rk4Step(x, r, k, dt float64) float64 {
	k1 := derivative(x, r, k)
	k2 := derivative(x+0.5*dt*k1, r, k)
	k3 := derivative(x+0.5*dt*k2, r, k)
	k4 := derivative(x+dt*k3, r, k)
	return math.Max(0.0, x+(dt/6.0)*(k1+2.0*k2+2.0*k3+k4))
}

func simulate(model LogisticModel) []float64 {
	states := make([]float64, 0, model.Steps+1)
	x := model.InitialState
	for step := 0; step <= model.Steps; step++ {
		states = append(states, x)
		x = rk4Step(x, model.GrowthRate, model.CarryingCapacity, model.Dt)
	}
	return states
}

func main() {
	model := LogisticModel{
		Name:             "go_baseline",
		InitialState:     10.0,
		GrowthRate:       0.35,
		CarryingCapacity: 100.0,
		Dt:               0.1,
		Steps:            160,
	}
	states := simulate(model)
	fmt.Printf("Go scenario=%s final_state=%.6f\n", model.Name, states[len(states)-1])
}
