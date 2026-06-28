package main

import "fmt"

func main() {
	rowCount := 4
	columnCount := 2
	overdetermined := true
	rank := 2
	residualNorm := 0.191311

	fmt.Println("system_name,row_count,column_count,overdetermined,rank,solution,fitted_values,residuals,residual_norm,warning")
	fmt.Printf("four_observation_linear_calibration,%d,%d,%t,%d,0.850000;1.040000,1.890000;2.930000;3.970000;5.010000,0.110000;-0.030000;0.130000;0.090000,%.6f,Least squares requires residual and model-purpose review.\n",
		rowCount, columnCount, overdetermined, rank, residualNorm)
}
