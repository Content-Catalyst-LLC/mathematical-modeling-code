#include <stdio.h>
#include <stdlib.h>

int main(void){
  printf("item,expression,interpretation,warning\n");
  printf("rate_expression,\"r*x*(1 - x/K)\",\"Logistic growth rate expression.\",\"K must be nonzero and domains documented.\"\n");
  printf("first_derivative,\"r - 2*r*x/K\",\"Marginal growth effect declines as x increases.\",\"Derivative signs depend on parameter regime.\"\n");
  printf("second_derivative,\"-2*r/K\",\"Curvature is negative for positive r and K.\",\"Curvature does not validate empirical structure.\"\n");
  printf("equilibria,\"x = 0 or x = K\",\"Candidate steady states.\",\"Equilibria require stability and domain review.\"\n");
  printf("limit_at_capacity,\"0\",\"Growth rate approaches zero at carrying capacity.\",\"Boundary behavior should be reviewed.\"\n");
  return EXIT_SUCCESS;
}
