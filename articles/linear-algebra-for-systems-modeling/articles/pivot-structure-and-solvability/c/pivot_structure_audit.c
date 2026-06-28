#include <stdio.h>

int main(void) {
    int equation_count = 3;
    int unknown_count = 3;
    int coefficient_rank = 3;
    int augmented_rank = 3;
    int consistent = 1;
    double tolerance = 1e-10;

    printf("system_name,equation_count,unknown_count,pivot_columns,free_columns,coefficient_rank,augmented_rank,consistent,solution_behavior,tolerance,warning\n");
    printf("three_constraint_resource_balance_system,%d,%d,0;1;2,none,%d,%d,%d,unique solution,%.10f,Pivot structure reveals algebraic solvability but feasibility requires review.\n",
           equation_count, unknown_count, coefficient_rank, augmented_rank, consistent, tolerance);
    return 0;
}
