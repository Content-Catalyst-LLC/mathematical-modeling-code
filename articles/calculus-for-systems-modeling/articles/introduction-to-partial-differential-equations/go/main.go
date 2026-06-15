package main

import "fmt"

func main() {
	gridPoints := 51
	steps := 100
	diffusivity := 0.1
	dx := 1.0
	dt := 0.25
	ratio := diffusivity * dt / (dx * dx)
	field := make([]float64, gridPoints)
	field[gridPoints/2] = 1.0

	fmt.Println("step,time,center_value,total_mass,max_value,min_value,stability_ratio,warning")
	for step := 0; step <= steps; step++ {
		totalMass := 0.0
		maxValue := field[0]
		minValue := field[0]
		for _, v := range field {
			totalMass += v * dx
			if v > maxValue {
				maxValue = v
			}
			if v < minValue {
				minValue = v
			}
		}
		fmt.Printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Explicit diffusion schemes require stability checks boundary and grid assumptions shape results.\n",
			step, float64(step)*dt, field[gridPoints/2], totalMass, maxValue, minValue, ratio)

		updated := make([]float64, gridPoints)
		copy(updated, field)
		for i := 1; i < gridPoints-1; i++ {
			updated[i] = field[i] + ratio*(field[i+1]-2*field[i]+field[i-1])
		}
		updated[0] = 0.0
		updated[gridPoints-1] = 0.0
		field = updated
	}
}
