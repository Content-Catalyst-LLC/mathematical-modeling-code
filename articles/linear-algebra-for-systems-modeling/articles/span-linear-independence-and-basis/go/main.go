package main

import (
	"fmt"
	"math"
)

func determinant3x3(m [3][3]float64) float64 {
	return m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1]) -
		m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0]) +
		m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0])
}

func main() {
	matrix := [3][3]float64{
		{1.0, 0.0, 0.5},
		{0.0, 1.0, 0.5},
		{0.0, 0.0, 1.0},
	}
	rank := 2
	if math.Abs(determinant3x3(matrix)) > 1e-10 {
		rank = 3
	}
	spans := rank == 3
	independent := rank == 3
	basis := spans && independent

	fmt.Println("vector_set_name,ambient_dimension,vector_count,rank,spans_ambient_space,linearly_independent,is_basis_for_ambient_space,warning")
	fmt.Printf("candidate_system_basis,3,3,%d,%t,%t,%t,A mathematical basis claim does not prove real-world adequacy.\n", rank, spans, independent, basis)
}
