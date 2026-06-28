#include <stdio.h>

int main(void) {
    int row_count = 4;
    int column_count = 4;
    int nonzero_entries = 8;
    double sparsity_ratio = 0.5;
    int symmetric = 1;
    int rank = 4;

    printf("matrix_name,matrix_role,row_count,column_count,nonzero_entries,sparsity_ratio,symmetric,rank,warning\n");
    printf("infrastructure_interdependency_matrix,weighted adjacency matrix,%d,%d,%d,%.4f,%d,%d,Symmetry should not be assumed unless system relationships are reciprocal.\n",
           row_count, column_count, nonzero_entries, sparsity_ratio, symmetric, rank);
    return 0;
}
