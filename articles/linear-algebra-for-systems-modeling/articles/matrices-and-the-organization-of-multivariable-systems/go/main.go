package main

import "fmt"

func main() {
	rowCount := 4
	columnCount := 4
	nonzeroEntries := 8
	sparsityRatio := 0.5
	symmetric := true
	rank := 4

	fmt.Println("matrix_name,matrix_role,row_count,column_count,nonzero_entries,sparsity_ratio,symmetric,rank,warning")
	fmt.Printf("infrastructure_interdependency_matrix,weighted adjacency matrix,%d,%d,%d,%.4f,%t,%d,Symmetry should not be assumed unless system relationships are reciprocal.\n",
		rowCount, columnCount, nonzeroEntries, sparsityRatio, symmetric, rank)
}
