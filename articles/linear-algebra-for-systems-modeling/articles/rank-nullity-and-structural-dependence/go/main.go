package main

import "fmt"

func main() {
	rowCount := 3
	columnCount := 3
	rank := 3
	nullity := columnCount - rank
	rankDeficient := false
	tolerance := 1.0e-10

	fmt.Println("system_name,row_count,column_count,rank,nullity,rank_deficient,pivot_columns,free_columns,tolerance,warning")
	fmt.Printf("three_constraint_resource_balance_matrix,%d,%d,%d,%d,%t,0;1;2,none,%.10f,Rank and nullity reveal structure but interpretation depends on model meaning.\n",
		rowCount, columnCount, rank, nullity, rankDeficient, tolerance)
}
