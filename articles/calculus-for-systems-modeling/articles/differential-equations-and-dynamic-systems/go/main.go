package main

import "fmt"

func exponentialRate(x, r float64) float64 { return r*x }
func logisticRate(x, r, k float64) float64 { return r*x*(1.0 - x/k) }

func simulate(scenario string, logistic bool) {
	x := 10.0
	r := 0.35
	k := 100.0
	dt := 0.1
	for n := 0; n <= 100; n++ {
		t := float64(n) * dt
		rate := exponentialRate(x, r)
		model := "dx_dt_equals_r_x"
		capacity := -1.0
		warning := "Exponential growth assumes no capacity constraint."
		if logistic {
			rate = logisticRate(x, r, k)
			model = "dx_dt_equals_r_x_one_minus_x_over_K"
			capacity = k
			warning = "Logistic growth assumes a fixed carrying capacity."
		}
		fmt.Printf("%s,%s,%.6f,%.6f,%.6f,%.6f,%.6f,explicit_euler,%s\n", scenario, model, t, x, rate, r, capacity, warning)
		x += dt * rate
	}
}

func main() {
	fmt.Println("scenario,model_type,time,state,rate,growth_rate,carrying_capacity,method,warning")
	simulate("exponential_growth", false)
	simulate("logistic_growth", true)
}
