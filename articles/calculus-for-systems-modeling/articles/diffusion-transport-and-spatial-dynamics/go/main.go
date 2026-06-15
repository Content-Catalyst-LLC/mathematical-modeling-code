package main

import "fmt"

func main() {
	gridPoints := 61
	steps := 120
	diffusivity := 0.08
	velocity := 0.4
	dx := 1.0
	dt := 0.2
	dRatio := diffusivity * dt / (dx * dx)
	tRatio := velocity * dt / dx
	field := make([]float64, gridPoints)
	field[gridPoints/2] = 1.0

	fmt.Println("step,time,center_value,total_mass,max_value,min_value,diffusion_ratio,transport_ratio,warning")
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
		fmt.Printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,Spatial dynamics depend on field meaning boundary conditions grid spacing time step and numerical stability.\n",
			step, float64(step)*dt, field[gridPoints/2], totalMass, maxValue, minValue, dRatio, tRatio)

		updated := make([]float64, gridPoints)
		copy(updated, field)
		for i := 1; i < gridPoints-1; i++ {
			diffusionPart := dRatio * (field[i+1] - 2*field[i] + field[i-1])
			transportPart := -tRatio * (field[i] - field[i-1])
			updated[i] = field[i] + diffusionPart + transportPart
		}
		updated[0] = 0.0
		updated[gridPoints-1] = 0.0
		field = updated
	}
}
