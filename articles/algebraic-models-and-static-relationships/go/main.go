package main

import "fmt"

type Scenario struct {
	Name        string
	Budget      float64
	CostA       float64
	CostB       float64
	BenefitA    float64
	BenefitB    float64
	AllocationA float64
	AllocationB float64
	CapacityA   float64
	CapacityB   float64
}

func evaluate(s Scenario) (totalCost float64, totalBenefit float64, benefitPerCost float64, budgetSlack float64, feasible bool) {
	totalCost = s.CostA*s.AllocationA + s.CostB*s.AllocationB
	totalBenefit = s.BenefitA*s.AllocationA + s.BenefitB*s.AllocationB
	budgetSlack = s.Budget - totalCost
	if totalCost > 0 {
		benefitPerCost = totalBenefit / totalCost
	}
	feasible = budgetSlack >= 0 && s.CapacityA-s.AllocationA >= 0 && s.CapacityB-s.AllocationB >= 0
	return
}

func main() {
	scenarios := []Scenario{
		{"go_balanced_feasible", 100, 4, 5, 8, 11, 10, 8, 20, 15},
		{"go_capacity_stress", 120, 4, 5, 8, 11, 25, 5, 20, 15},
	}

	for _, scenario := range scenarios {
		totalCost, totalBenefit, benefitPerCost, budgetSlack, feasible := evaluate(scenario)
		fmt.Printf("%s total_cost=%.3f total_benefit=%.3f benefit_per_cost=%.3f budget_slack=%.3f feasible=%v\n",
			scenario.Name, totalCost, totalBenefit, benefitPerCost, budgetSlack, feasible)
	}
}
