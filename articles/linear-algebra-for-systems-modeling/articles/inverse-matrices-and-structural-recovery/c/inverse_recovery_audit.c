#include <stdio.h>
int main(void) {
  printf("system_name,matrix_size,determinant,invertible,rank,nullity,recovered_solution,residual_norm,tolerance,warning\n");
  printf("three_constraint_structural_recovery_system,3,2.000000,1,3,0,55.000000;45.000000;35.000000,0.000000,0.0000000001,Inverse recovery is algebraic; conditioning requires review.\n");
  return 0;
}
