#include <iostream>
#include <iomanip>

int main() {
    int equation_count = 3;
    int unknown_count = 3;
    int coefficient_rank = 3;
    int augmented_rank = 3;
    bool consistent = true;
    double tolerance = 1e-10;

    std::cout << "system_name,equation_count,unknown_count,pivot_columns,free_columns,coefficient_rank,augmented_rank,consistent,solution_behavior,tolerance,warning\n";
    std::cout << "three_constraint_resource_balance_system,"
              << equation_count << "," << unknown_count << ",0;1;2,none,"
              << coefficient_rank << "," << augmented_rank << ","
              << consistent << ",unique solution,"
              << std::setprecision(12) << tolerance
              << ",Pivot structure reveals algebraic solvability but feasibility requires review.\n";
    return 0;
}
