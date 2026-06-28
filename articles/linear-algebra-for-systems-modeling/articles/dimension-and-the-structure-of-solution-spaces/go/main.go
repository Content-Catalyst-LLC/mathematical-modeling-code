package main

import "fmt"

func main() {
	variableCount := 4
	equationCount := 3
	rank := 3
	nullity := variableCount - rank

	fmt.Println("system_name,variable_count,equation_count,rank,nullity,likely_solution_structure,warning")
	fmt.Printf("four_variable_three_constraint_system,%d,%d,%d,%d,Positive-dimensional solution space if consistent,Rank and nullity are mathematical diagnostics not proof of feasibility.\n",
		variableCount, equationCount, rank, nullity)
}
