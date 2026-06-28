package main

import "fmt"

func main() {
	equationCount := 3
	unknownCount := 3
	coefficientRank := 3
	augmentedRank := 3
	consistent := true

	fmt.Println("system_name,equation_count,unknown_count,coefficient_rank,augmented_rank,consistent,solution_behavior,warning")
	fmt.Printf("three_constraint_resource_balance_system,%d,%d,%d,%d,%t,unique solution,Algebraic consistency does not guarantee practical feasibility.\n",
		equationCount, unknownCount, coefficientRank, augmentedRank, consistent)
}
