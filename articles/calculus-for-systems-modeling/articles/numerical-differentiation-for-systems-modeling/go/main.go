package main

import (
	"fmt"
	"math"
)

func signal(x float64) float64 {
	return math.Sin(x) + 0.1*x*x
}

func trueDerivative(x float64) float64 {
	return math.Cos(x) + 0.2*x
}

func main() {
	start := 0.0
	stop := 10.0
	h := 0.1
	n := int(math.Round((stop - start) / h))
	xs := make([]float64, n+1)
	values := make([]float64, n+1)

	for i := 0; i <= n; i++ {
		xs[i] = start + float64(i)*h
		values[i] = signal(xs[i])
	}

	fmt.Println("index,x,value,true_derivative,forward_difference,backward_difference,central_difference,central_absolute_error,step_size,warning")
	for i := 0; i <= n; i++ {
		forward := math.NaN()
		backward := math.NaN()
		central := math.NaN()
		err := math.NaN()

		if i < n {
			forward = (values[i+1] - values[i]) / h
		}
		if i > 0 {
			backward = (values[i] - values[i-1]) / h
		}
		if i > 0 && i < n {
			central = (values[i+1] - values[i-1]) / (2 * h)
			err = math.Abs(central - trueDerivative(xs[i]))
		}

		fmt.Printf("%d,%.6f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.6f,Numerical derivatives depend on step size formula choice boundary handling smoothness and noise.\n",
			i, xs[i], values[i], trueDerivative(xs[i]), forward, backward, central, err, h)
	}
}
