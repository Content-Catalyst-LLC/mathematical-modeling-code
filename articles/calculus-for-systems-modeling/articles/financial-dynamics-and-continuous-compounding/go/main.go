package main

import (
	"fmt"
	"math"
)

func continuousFutureValue(v0, r, t float64) float64 {
	return v0 * math.Exp(r*t)
}

func continuousPresentValue(fv, r, t float64) float64 {
	return fv * math.Exp(-r*t)
}

func main() {
	fmt.Println("scenario_name,model_type,final_value,present_value,warning")
	fmt.Printf("continuous_compounding_case,future_value,%.6f,1000.000000,continuous_compounding\n", continuousFutureValue(1000.0, 0.05, 30.0))
	fmt.Printf("discounted_future_value,present_value,5000.000000,%.6f,discounting\n", continuousPresentValue(5000.0, 0.05, 30.0))
}
