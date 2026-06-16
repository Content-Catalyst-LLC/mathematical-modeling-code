package main

import "fmt"

type ModelParameters struct {
	GrowthRate       float64
	CarryingCapacity float64
	InitialStock     float64
	TimeStep          float64
	Horizon           float64
}

type ModelState struct {
	ModelTime float64
	Stock     float64
}

func stepLogistic(p ModelParameters, s ModelState) ModelState {
	dx := p.GrowthRate * s.Stock * (1 - s.Stock/p.CarryingCapacity)
	return ModelState{ModelTime: s.ModelTime + p.TimeStep, Stock: s.Stock + p.TimeStep*dx}
}

func main() {
	p := ModelParameters{GrowthRate: 0.35, CarryingCapacity: 100, InitialStock: 10, TimeStep: 0.25, Horizon: 20}
	s := ModelState{ModelTime: 0, Stock: p.InitialStock}
	for s.ModelTime < p.Horizon {
		s = stepLogistic(p, s)
	}
	fmt.Println("model_use,growth_rate,carrying_capacity,initial_stock,time_step,horizon,final_time,final_stock,warning")
	fmt.Printf("governance_review,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.12f,Typed records improve structural review but do not prove empirical validity.\n",
		p.GrowthRate, p.CarryingCapacity, p.InitialStock, p.TimeStep, p.Horizon, s.ModelTime, s.Stock)
}
