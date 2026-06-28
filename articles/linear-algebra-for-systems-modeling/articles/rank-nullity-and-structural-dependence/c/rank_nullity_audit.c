#include <stdio.h>

int main(void) {
    int row_count = 3;
    int column_count = 3;
    int rank = 3;
    int nullity = column_count - rank;
    int rank_deficient = 0;
    double tolerance = 1e-10;

    printf("system_name,row_count,column_count,rank,nullity,rank_deficient,pivot_columns,free_columns,tolerance,warning\n");
    printf("three_constraint_resource_balance_matrix,%d,%d,%d,%d,%d,0;1;2,none,%.10f,Rank and nullity reveal structure but interpretation depends on model meaning.\n",
           row_count, column_count, rank, nullity, rank_deficient, tolerance);
    return 0;
}
