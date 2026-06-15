package main

import (
	"fmt"
	"math"
)

func restoringRate(x, equilibrium, recoveryRate float64) float64 {
	return -recoveryRate * (x - equilibrium)
}

func impulseShock(time, shockTime, shockMagnitude float64) float64 {
	if math.Abs(time-shockTime) < 1e-12 {
		return shockMagnitude
	}
	return 0
}

func main() {
	baseline := 100.0
	forced := 100.0
	equilibrium := 100.0
	recoveryRate := 0.15
	shockTime := 10.0
	shockMagnitude := -30.0
	dt := 0.1

	fmt.Println("step,time,baseline_state,forced_state,shock_value,absolute_deviation,warning")
	for step := 0; step <= 300; step++ {
		time := float64(step) * dt
		shock := impulseShock(time, shockTime, shockMagnitude)
		fmt.Printf("%d,%.6f,%.6f,%.6f,%.6f,%.6f,Shock response depends on forcing form timing magnitude recovery rate and numerical step size.\n", step, time, baseline, forced, shock, math.Abs(forced-baseline))
		baseline = baseline + dt*restoringRate(baseline, equilibrium, recoveryRate)
		if shock != 0 {
			forced += shock
		}
		forced = forced + dt*restoringRate(forced, equilibrium, recoveryRate)
	}
}
