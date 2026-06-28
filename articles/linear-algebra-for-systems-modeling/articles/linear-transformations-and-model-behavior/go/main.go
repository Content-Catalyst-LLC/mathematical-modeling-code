package main

import "fmt"

func main() {
	rowCount := 3
	columnCount := 3
	rank := 3
	nullity := 0
	inputNorm := 120.415946
	outputNorm := 152.750205
	amplificationRatio := outputNorm / inputNorm

	fmt.Println("system_name,row_count,column_count,input_state,output_state,rank,nullity,input_norm,output_norm,amplification_ratio,warning")
	fmt.Printf("three_component_system_response,%d,%d,100.000000;60.000000;30.000000,126.000000;75.500000;42.000000,%d,%d,%.6f,%.6f,%.6f,Matrix action requires row meanings column meanings units scaling and sensitivity review.\n",
		rowCount, columnCount, rank, nullity, inputNorm, outputNorm, amplificationRatio)
}
