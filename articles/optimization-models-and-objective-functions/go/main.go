package main

import "fmt"

type Program struct {
	Name    string
	Benefit float64
	Cost    float64
	Lower   int
	Upper   int
}

type Scenario struct {
	Name        string
	Budget      float64
	EquityFloor int
}

func evaluate(allocation []int, programs []Program, scenario Scenario) (float64, float64, bool) {
	totalCost := 0.0
	totalBenefit := 0.0
	equityOK := true

	for i, units := range allocation {
		totalCost += float64(units) * programs[i].Cost
		totalBenefit += float64(units) * programs[i].Benefit
		if units < scenario.EquityFloor {
			equityOK = false
		}
	}

	return totalCost, totalBenefit, totalCost <= scenario.Budget && equityOK
}

func main() {
	programs := []Program{
		{"housing", 11, 7, 0, 8},
		{"health", 13, 8, 0, 8},
		{"transport", 8, 5, 0, 8},
		{"resilience", 10, 6, 0, 8},
	}
	scenario := Scenario{"go_baseline", 75, 1}

	bestBenefit := -1.0
	bestAllocation := []int{}
	feasibleCount := 0
	candidateCount := 0

	for a := 0; a <= 8; a++ {
		for b := 0; b <= 8; b++ {
			for c := 0; c <= 8; c++ {
				for d := 0; d <= 8; d++ {
					allocation := []int{a, b, c, d}
					_, benefit, feasible := evaluate(allocation, programs, scenario)
					candidateCount++
					if feasible {
						feasibleCount++
						if benefit > bestBenefit {
							bestBenefit = benefit
							bestAllocation = allocation
						}
					}
				}
			}
		}
	}

	fmt.Printf("%s candidates=%d feasible=%d best_benefit=%.2f best_allocation=%v\n",
		scenario.Name, candidateCount, feasibleCount, bestBenefit, bestAllocation)
}
