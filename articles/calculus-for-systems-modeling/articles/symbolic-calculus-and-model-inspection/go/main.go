package main

import "fmt"

func main() {
	fmt.Println("item,expression,interpretation,warning")
	fmt.Println("rate_expression,\"r*x*(1 - x/K)\",\"Logistic growth rate expression.\",\"K must be nonzero and domains documented.\"")
	fmt.Println("first_derivative,\"r - 2*r*x/K\",\"Marginal growth effect declines as x increases.\",\"Derivative signs depend on parameter regime.\"")
	fmt.Println("second_derivative,\"-2*r/K\",\"Curvature is negative for positive r and K.\",\"Curvature does not validate empirical structure.\"")
	fmt.Println("equilibria,\"x = 0 or x = K\",\"Candidate steady states.\",\"Equilibria require stability and domain review.\"")
	fmt.Println("limit_at_capacity,\"0\",\"Growth rate approaches zero at carrying capacity.\",\"Boundary behavior should be reviewed.\"")
}
