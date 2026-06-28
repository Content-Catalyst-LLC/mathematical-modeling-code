#include <iostream>

int main() {
    int row_count = 4;
    int column_count = 4;
    int nonzero_entries = 8;
    double sparsity_ratio = 0.5;
    bool symmetric = true;
    int rank = 4;

    std::cout << "matrix_name,matrix_role,row_count,column_count,nonzero_entries,sparsity_ratio,symmetric,rank,warning\n";
    std::cout << "infrastructure_interdependency_matrix,weighted adjacency matrix,"
              << row_count << "," << column_count << "," << nonzero_entries << ","
              << sparsity_ratio << "," << symmetric << "," << rank
              << ",Symmetry should not be assumed unless system relationships are reciprocal.\n";
    return 0;
}
