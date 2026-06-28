#include <stdio.h>

int main(void) {
    int variable_count = 4;
    int equation_count = 3;
    int rank = 3;
    int nullity = variable_count - rank;

    printf("system_name,variable_count,equation_count,rank,nullity,likely_solution_structure,warning\n");
    printf("four_variable_three_constraint_system,%d,%d,%d,%d,Positive-dimensional solution space if consistent,Rank and nullity are mathematical diagnostics not proof of feasibility.\n",
           variable_count, equation_count, rank, nullity);
    return 0;
}
