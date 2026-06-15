package main

import "fmt"

func rates(prey, predator, alpha, beta, delta, gamma float64) (float64, float64) {
	return alpha*prey - beta*prey*predator, delta*prey*predator - gamma*predator
}

func max(a, b float64) float64 {
	if a > b {
		return a
	}
	return b
}

func main() {
	prey := 40.0
	predator := 9.0
	alpha := 0.7
	beta := 0.05
	delta := 0.02
	gamma := 0.5
	dt := 0.01
	fmt.Println("scenario,time,prey,predator,prey_rate,predator_rate,alpha,beta,delta,gamma,method,warning")
	for n := 0; n <= 2000; n++ {
		t := float64(n) * dt
		preyRate, predatorRate := rates(prey, predator, alpha, beta, delta, gamma)
		fmt.Printf("predator_prey_coupled_system,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,explicit_euler,Predator-prey terms are illustrative and assume continuous well-mixed interaction.\n", t, prey, predator, preyRate, predatorRate, alpha, beta, delta, gamma)
		prey = max(0, prey+dt*preyRate)
		predator = max(0, predator+dt*predatorRate)
	}
}
