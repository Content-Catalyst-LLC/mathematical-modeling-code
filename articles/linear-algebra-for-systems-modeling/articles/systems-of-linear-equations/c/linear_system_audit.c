#include <stdio.h>

int main(void) {
    int equation_count = 3;
    int unknown_count = 3;
    int coefficient_rank = 3;
    int augmented_rank = 3;
    int consistent = 1;

    printf("system_name,equation_count,unknown_count,coefficient_rank,augmented_rank,consistent,solution_behavior,warning\n");
    printf("three_constraint_resource_balance_system,%d,%d,%d,%d,%d,unique solution,Algebraic consistency does not guarantee practical feasibility.\n",
           equation_count, unknown_count, coefficient_rank, augmented_rank, consistent);
    return 0;
}
