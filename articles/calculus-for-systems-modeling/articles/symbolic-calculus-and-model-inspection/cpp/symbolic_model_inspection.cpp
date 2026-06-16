#include <iostream>

int main(){
  std::cout << "item,expression,interpretation,warning\n";
  std::cout << "rate_expression,\"r*x*(1 - x/K)\",\"Logistic growth rate expression.\",\"K must be nonzero and domains documented.\"\n";
  std::cout << "first_derivative,\"r - 2*r*x/K\",\"Marginal growth effect declines as x increases.\",\"Derivative signs depend on parameter regime.\"\n";
  std::cout << "second_derivative,\"-2*r/K\",\"Curvature is negative for positive r and K.\",\"Curvature does not validate empirical structure.\"\n";
  std::cout << "equilibria,\"x = 0 or x = K\",\"Candidate steady states.\",\"Equilibria require stability and domain review.\"\n";
  std::cout << "limit_at_capacity,\"0\",\"Growth rate approaches zero at carrying capacity.\",\"Boundary behavior should be reviewed.\"\n";
}
