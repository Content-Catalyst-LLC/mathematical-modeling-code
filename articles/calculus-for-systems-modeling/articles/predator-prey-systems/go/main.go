package main

import "fmt"

func main() {
	alpha, beta, gamma, delta := 0.6, 0.02, 0.5, 0.01
	x, y, dt := 40.0, 9.0, 0.02
	for i := 0; i < 4000; i++ {
		dx := alpha*x - beta*x*y
		dy := delta*x*y - gamma*y
		x += dt * dx
		y += dt * dy
		if x < 0 {
			x = 0
		}
		if y < 0 {
			y = 0
		}
	}
	fmt.Println("scenario_name,model_type,final_prey,final_predator,warning")
	fmt.Printf("classic_lotka_volterra,lotka_volterra,%.6f,%.6f,mass_action_baseline\n", x, y)
}
