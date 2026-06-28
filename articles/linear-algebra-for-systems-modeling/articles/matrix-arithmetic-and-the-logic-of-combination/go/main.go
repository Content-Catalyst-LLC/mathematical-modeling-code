package main

import "fmt"

func main() {
	compatibleShape := true
	outputEntrySum := 3.95

	fmt.Println("operation_name,matrix_shape,compatible_shape,output_entry_sum,warning")
	fmt.Printf("baseline_plus_weighted_intervention_and_stress,3x3,%t,%.4f,Shape compatibility is not enough; semantic compatibility must be documented.\n",
		compatibleShape, outputEntrySum)
}
