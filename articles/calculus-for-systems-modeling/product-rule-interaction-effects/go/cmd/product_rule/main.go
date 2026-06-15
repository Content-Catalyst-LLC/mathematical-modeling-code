package main

import "fmt"

type ProductContribution struct {
	ContributionFromA float64
	ContributionFromB float64
	TotalDerivative   float64
}

func ProductRule(a, b, da, db float64) ProductContribution {
	ca := da * b
	cb := a * db
	return ProductContribution{ca, cb, ca + cb}
}

func main() {
	fmt.Printf("%+v\n", ProductRule(120.0, 1.5, 4.0, 0.03))
}
