#include <iostream>
#include <iomanip>

int main() {
    int row_count = 3;
    int column_count = 3;
    int rank = 3;
    int nullity = column_count - rank;
    bool rank_deficient = false;
    double tolerance = 1e-10;

    std::cout << "system_name,row_count,column_count,rank,nullity,rank_deficient,pivot_columns,free_columns,tolerance,warning\n";
    std::cout << "three_constraint_resource_balance_matrix,"
              << row_count << "," << column_count << ","
              << rank << "," << nullity << ","
              << rank_deficient << ",0;1;2,none,"
              << std::setprecision(12) << tolerance
              << ",Rank and nullity reveal structure but interpretation depends on model meaning.\n";
    return 0;
}
